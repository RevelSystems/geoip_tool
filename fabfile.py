import getpass
from fabric.operations import put
from fabric.state import env

ATLAS_DEFAULT_USER = 'root'

if env.user == getpass.getuser():
    env.user = ATLAS_DEFAULT_USER

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

def deploy(path="/var/www/press/"):
    """Deploys ip tool to remote server."""
    put("geo.db", path)
    put("geo.php", path)
    put("Spyc.php", path)