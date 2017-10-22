#!python/bin/python
from app import app
#from werkzeug.contrib.fixers import ProxyFix, CGIRootFix

#app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
#app = CGIRootFix(app, app_root='/')

if __name__ == '__main__':
    app.run(debug=False)
