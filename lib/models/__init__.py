import os
dirlist = sorted(os.listdir(os.path.dirname(__file__)))
import_files = [d for d in dirlist if d.endswith('.py') and not d.startswith('__init__')]

for d in import_files:
    __import__('models.%s' % d.replace('.py', ''))
