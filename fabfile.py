from fabric.api import env, local, cd, run, prefix

env.hosts = ['sdelquin.me']


def deploy():
    local('git push')
    with prefix('source ~/.pyenv/versions/cifutils/bin/activate'):
        with cd('~/code/cifutils'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('python manage.py collectstatic --noinput')
            run('supervisorctl restart cifutils')
