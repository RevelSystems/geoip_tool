import getpass
import os
from fabric.operations import put, sudo, local
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
            'www1': 'revelweb.revelup.com'
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
        "#BEGIN RevelIP\n",
        "<IfModule mod_rewrite.c>\n"
        "RewriteEngine On\n",
        "RewriteBase /\n",
        "RewriteRule ^index\.php$ /geo.php [L]\n",
        "</IfModule>\n",
        "#End RevelIP\n"
    ]

    with download(remote_path) as local_file_name:
        with open(local_file_name, 'r') as f:
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

        with open(local_file_name, 'w') as f:
            f.write("".join(result_config))

        put(local_file_name, remote_path)
        sudo("chown %s:%s %s" % (WWW_USER, WWW_USER, remote_path))
        local("cat %s" % local_file_name)

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