import sys, os
sys.path.insert(0, '/home/productizer/myproject/Olivia/service')
sys.path.append('/usr/local/cuda/bin')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))

from App import app as application
