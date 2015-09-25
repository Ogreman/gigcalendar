import os
from fabric.api import local, settings, run, env, cd

env.use_ssh_config = True
env.hosts = ['raffers']
postactivate = os.environ['VIRTUAL_ENV'] + '/bin/postactivate'
project_path = os.environ['REMOTE_PROJECT_PATH']
tools_file = "/usr/local/lib/python2.7/dist-packages/oauth2client/tools.py"


def mkdirs():
    run("mkdir -p %s" % project_path)


def start():
    with settings(warn_only=True):
        with cd(project_path):
            run('source postactivate && dtach -n `mktemp -u /tmp/dtach.XXXX` python %s/app.py' % project_path)


def commit(words):
    with settings(warn_only=True):
        local("git add -u && git commit -m '%s'" % words)


def push(branch="master"):
    with settings(warn_only=True):
        local("git push %s %s" % (env.hosts[0], branch))


def prepare(branch="_dummy", stash=True):
    with cd(project_path):
        if stash:
            run("git stash")
        with settings(warn_only=True):
            result = run("git checkout -b %s" % branch)
        if result.failed:
            run("git checkout %s" % branch)


def finalise(branch="master", stash=True):
    with cd(project_path):
        run("git checkout %s" % branch)
        if stash:
            run("git stash pop")


def clean(branch="_dummy"):
    with cd(project_path):
        with settings(warn_only=True):
            run("git branch -D %s" % branch)


def kill():
    pid = run("ps aux | grep gig | grep -v grep | awk '{print $2}'")
    for p in pid.split('\n'):
        if p:
            run("kill %d" % int(p))


def running():
    run("ps aux | grep gig | grep -v grep | awk '{print $2}'")


def logs():
    with cd(project_path):
        return run("tail gigs.log")


def rmdirs(prompt=True):
    if not prompt:
        run("rm -rf %s" % project_path)
        return
    if confirm("Delete everything?"):
        run("rm -rf %s" % project_path)


def initgit():
    with cd(project_path):
        run("git init")


def scpfiles():
    local("scp %s raffers:/home/james/projects/gig/" % postactivate)
    local("scp client_secret.json raffers:/home/james/projects/gig/")
    local("scp tools.py raffers:%s" % tools_file)


def prod():
    with cd(project_path):
        run("echo export GIG_PRODUCTION=True >> postactivate")


def installdeps():
    with settings(warn_only=True):
        with cd(project_path):
            run("pip install -r requirements.txt")


def new():
    kill()
    mkdir()
    initgit()
    prepare(stash=False)
    push()
    finalise(stash=False)
    clean()
    installdeps()
    scpfiles()
    prod()
    start()


def refresh():
    kill()
    rmdirs(prompt=False)
    new()


def deploy(m):
    commit(m)
    kill()
    prepare()
    push()
    finalise()
    clean()
    start()
