from fabric.api import *
from fabric.context_managers import settings

env.user = 'ubuntu'
env.key_filename = ['key.pem']

def _get_manage_dot_py(host):
    '''получить manage.py'''

    return f'/home/{env.user}/sites/{host}/virtualenv/bin/python /home/{env.user}/sites/{host}/source/manage.py'

def reset_database(host):
    '''обнулить базу данных'''

    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{env.user}@{host}'):
        run(f'{manage_dot_py} flush --noinput')

def create_session_on_server(host, email):
    '''создать сеанс на сервере'''

    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{env.user}@{host}'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()