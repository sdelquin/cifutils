from fabric.api import env, local, cd, run, prefix

env.hosts = ['cloud']


def deploy():
    local('git push')
    with prefix('source ~/.virtualenvs/cifutils/bin/activate'):
        with cd('~/cifutils'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('python manage.py collectstatic --noinput')
            run('supervisorctl restart cifutils')
