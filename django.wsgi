import os, sys  
sys.path.append('C:/windows/www/bright/bfc/')
sys.path.append('C:/windows/www/bright')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'  
import django.core.handlers.wsgi  
application = django.core.handlers.wsgi.WSGIHandler()  
