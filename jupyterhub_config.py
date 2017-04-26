# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


# Configuration file for JupyterHub
import os

BASE_WORK_DIR = '/home/jenkins/'

c = get_config()

# ABSOLUTE URLs!!!
c.JupyterHub.base_url = '/jupyter-alfa/'

# Set the log level by value or name.
#c.JupyterHub.log_level = 'DEBUG'
#c.Spawner.debug = True

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
#c.DockerSpawner.volumes = { 'jupyterhub-user-shared': notebook_dir }
c.DockerSpawner.volumes = { BASE_WORK_DIR + 'jupyter-user-work': notebook_dir }
c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
# Add alfasim prototypes
c.DockerSpawner.read_only_volumes = { BASE_WORK_DIR + 'alfasim-prototypes': '/alfasim-prototypes' }
c.DockerSpawner.environment = { 'PYTHONPATH': '/alfasim-prototypes/alfasim:/alfasim-prototypes/alfasim/prototypes' } 

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config
#c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']
#c.JupyterHub.port = 80
c.JupyterHub.port = 8765


c.JupyterHub.authenticator_class = 'json_auth.JsonAuthenticator'
c.JsonAuthenticator.passwords_file = os.environ['PASSWD']

## Authenticate users with GitHub OAuth
#c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
#c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

## Using ldap
#c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
#c.LDAPAuthenticator.server_address = '10.0.0.1'
#c.LDAPAuthenticator.bind_dn_template = 'uid={username},ou=Users,ou=EXAMPLE,dc=example,dc=com'
##c.LDAPAuthenticator.use_ssl = False

## Testing
#c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
c.JupyterHub.db_url = os.path.join('sqlite:///', data_dir, 'jupyterhub.sqlite')
c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

# Whitlelist users and admins
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True
pwd = os.path.dirname(__file__)
with open(os.path.join(pwd, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

