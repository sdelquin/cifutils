from fabric.api import env, local, cd, run

env.hosts = ['cloud']


def deploy():
    local('git push')
    with cd('~/cifutils'):
        run('git pull')
        run('pipenv install')
        run('pipenv run python manage.py collectstatic --noinput')
        run('supervisorctl restart cifutils')
