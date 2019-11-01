### Para correr se debe tener las siguientes librerias
django-tenants
psycopg2
django-bootstrap4
django-role-permissions
django-tenants-schemas
*(usar `pip install [liberias]` para ello)*

### Dentro del proyecto hacer
- `python manage.py makemigrations`
- `python manage.py migrate_schemas --shared`
- `python manage.py createsuperuser` (para administrar franquicias)

### Correr los siguientes scripts SQL dentro de la base de datos
```SQL
INSERT INTO "franquicias_tipofranquicia" ("nombre","precio") VALUES ('basico',79);
INSERT INTO "franquicias_tipofranquicia" ("nombre","precio") VALUES ('premium',135);
INSERT INTO "franquicias_franquicia" ("schema_name", "nombre","fecha_corte","tipo_id") VALUES ('public', 'public',CURRENT_DATE,1);
INSERT INTO "franquicias_dominio" ("domain", "is_primary", "tenant_id") VALUES ('localhost', true, 1);
```