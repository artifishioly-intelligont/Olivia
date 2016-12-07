import os, site, sys

sys.path.insert(0, '/home/productizer/myproject/Olivia/service')

os.chdir("/home/productizer/myproject/Olivia/service")

site.addsitedir('/home/productizer/system-git-repos/neon/.venv2/lib/python2.7/site-packages')

#activate_env=os.path.expanduser("/home/productizer/system-git-repos/neon/.venv/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(BASE_DIR)

#def application(environ, start_response):
 #   for key in ['DB_NAME', 'DB_USER', 'DB_PASSWD', 'DB_HOST', 'SECRET_KEY', ]:
  #      os.environ[key] = environ.get(key, '')
from App import app as application

   # return _application(environ, start_response)
