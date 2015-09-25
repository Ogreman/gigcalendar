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


def start_app(path):
    with settings(warn_only=True):
        run('nohup python %s/app.py &' % env.REMOTE_PROJECT_PATH)


def commit(words):
    local("git add -u && git commit -m '%s'" % words)


def push(branch="master"):
    local("git push %s %s" % (env.hosts[0], branch))


def prepare(branch="_dummy"):
    with cd(env.REMOTE_PROJECT_PATH):
        run("git stash")
        result = run("git checkout -b %s" % branch)
        if result.failed:
            run("git checkout %s" % branch)


def finalise():
    with cd(env.REMOTE_PROJECT_PATH):
        run("git stash pop")


def clean(branch="_dummy"):
    with cd(env.REMOTE_PROJECT_PATH):
        with settings(warn_only=True):
            run("git branch -D %s" % branch)


def deploy(m):
    init_envs()
    commit(m)
    prepare()
    push()
    clean()
    finalise()
    start_app()
