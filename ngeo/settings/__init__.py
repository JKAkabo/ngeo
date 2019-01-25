import os

env = os.environ.setdefault('DJANGO_ENVIRONMENT', 'development')
if env in ('development', 'production', 'staging'):
    exec(f'from .{env} import *')
