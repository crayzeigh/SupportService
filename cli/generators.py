"""Generator Module.

Generates templates using jinja.
"""
import os
import uuid
from jinja2 import Environment, PackageLoader


class ConfigGenerator():
    """Abstract configuration generator using Jinja"""

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('cli', 'templates')
        )

    def generate_relay_config(self, environments):
        """Generate docker-compose.relay.yml."""
        template = self.env.get_template('docker-compose.relay.jinja')

        with open('docker-compose.relay.yml', 'w+') as docker_compose_file:
            t = template.render(
                envs = environments,
                redis_host = os.environ.get("LD_RELAY_REDIS_HOST")
            )
            docker_compose_file.write(t)

    def generate_prod_config(self, environments):
        """Generate production docker-compose."""
        template = self.env.get_template('docker-compose.prod.jinja')

        with open('docker-compose.prod.yml', 'w+') as docker_compose_file:
            t = template.render(
                envs = environments,
                circle_sha1 = os.environ.get('CIRCLE_SHA1') or 'latest'
            )
            docker_compose_file.write(t)

    def generate_nginx_config(self, environments):
        """Generate Nginx Config."""
        template = self.env.get_template('nginx.conf.jinja')

        with open('etc/nginx/nginx.conf', 'w+') as nginx_file:
            t = template.render(
                envs = environments
            )
            nginx_file.write(t)