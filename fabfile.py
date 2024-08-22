from fabric.api import cd, env, local, prefix, run

env.hosts = ['sdelquin.me']


def deploy():
    local('git push')
    with prefix('source .venv/bin/activate'):
        with cd('~/code/cifutils'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('python manage.py collectstatic --noinput')
            run('supervisorctl restart cifutils')
