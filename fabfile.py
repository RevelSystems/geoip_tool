import getpass
import os
from fabric.operations import put, sudo
from fabric.state import env
from utils.download import download

DEFAULT_USER = 'root'
WWW_USER = 'www-data'
DEFAULT_PATH = "/var/www/press/"

if env.user == getpass.getuser():
    env.user = DEFAULT_USER

hostmaps = \
    {
        'production':
        {
            'www1': 'www1.revelsystems.com',
            'www2': 'www2.revelsystems.com',
            'au': 'au.revelsystems.com'
        },
        'development':
        {
            'development': '198.58.99.187'
        },
    }

for (role, hosts) in hostmaps.iteritems():
    env.roledefs[role] = hosts.values()

def rewrite_rules(path=DEFAULT_PATH):
    """Deploys rewrite rules."""
    remote_path = os.path.join(path, ".htaccess")

    geo_config = [
        "#BEGIN RevelIP",
        "<IfModule mod_rewrite.c>"
        "RewriteEngine On",
        "RewriteBase /",
        "RewriteRule ^index\.php$ /geo.php [L]",
        "</IfModule>",
        "#End RevelIP",
    ]

    with download(remote_path) as local:
        with open(local, 'r') as f:
            content = f.readlines()
        result_config = []
        skip_mode = False
        for l in content:
            if "BEGIN RevelIP" in l:
                skip_mode = True
                continue
            if "End RevelIP" in l:
                skip_mode = False
                continue
            if skip_mode:
                continue

            if "BEGIN WordPress" in l:
                result_config.extend(geo_config)
            result_config.append(l)

        with open(local, 'w') as f:
            f.write("".join(content))

        put(local, remote_path)
        sudo("chown %s:%s %s" % (WWW_USER, WWW_USER, remote_path))

def deploy(path=DEFAULT_PATH):
    """Deploys ip tool to remote server."""
    files = [
        "geo.db",
        "geo.php",
        "Spyc.php"
    ]

    for file in files:
        put(file, path)
        sudo("chown %s:%s %s" % (WWW_USER, WWW_USER, os.path.join(path, file)))

    rewrite_rules(path=path)