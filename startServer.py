import os
os.system(f"gunicorn watchcool.wsgi -b=127.0.0.1:8005 --timeout={60*5} --workers=5 --threads=2 --daemon")