### Para correr se debe tener las siguientes librerias
- Django
- django-tenants
- psycopg2
- django-bootstrap4
- django-role-permissions
- django-tenant-schemas
- django-allauth
- pillow
- django-countries
- *(usar **`pip install -r requirements.txt`** para ello)*

### Dentro del proyecto hacer
``` shell
python manage.py migrate_schemas --shared
python manage.py createsuperuser
```