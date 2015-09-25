from fabric.api import local, settings, run, env, cd

env.use_ssh_config = True
env.hosts = ['raffers']


def init_envs():
    with open('/home/james/.virtualenvs/gigcalendar/bin/postactivate', 'r') as pa:
        for line in pa:
            try:
                key, val = line.split('=')
                key = key.split(' ')[1]
                env[key] = val.replace('"', '')
            except (IndexError, ValueError):
                pass


def start_app():
    with settings(warn_only=True):
        run('nohup python %s/app.py &' % env.REMOTE_PROJECT_PATH)


def commit(words):
    local("git add -u && git commit -m '%s'" % words)


def push(branch="master"):
    local("git push %s %s" % (env.hosts[0], branch))


def prepare(branch="_dummy"):
    with cd(env.REMOTE_PROJECT_PATH):
        run("git stash")
        with settings(warn_only=True):
            result = run("git checkout -b %s" % branch)
        if result.failed:
            run("git checkout %s" % branch)


def finalise(branch="master"):
    with cd(env.REMOTE_PROJECT_PATH):
        run("git checkout %s" % branch)
        run("git stash pop")


def clean(branch="_dummy"):
    with cd(env.REMOTE_PROJECT_PATH):
        with settings(warn_only=True):
            run("git branch -D %s" % branch)


def kill():
    pid = run("ps aux | grep gig | grep -v grep | awk '{print $2}'")
    if pid:
        run("kill %d" % int(pid))


def deploy(m):
    init_envs()
    commit(m)
    kill()
    prepare()
    push()
    finalise()
    clean()
    start_app()
