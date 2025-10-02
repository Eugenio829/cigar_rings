import os
import sys

# Añade la ruta de tu proyecto al sistema.
# Asegúrate de que la ruta '/home/Eugeniojiemenz17/cigar_rings' apunta
# al directorio que contiene tu archivo manage.py.
path = '/home/Eugeniojiemenz17/cigar_rings'
if path not in sys.path:
    sys.path.insert(0, path)

# Apunta a tu archivo de settings.
# La carpeta que contiene settings.py se llama 'config', por eso es 'config.settings'.
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Carga la aplicación WSGI de Django.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()