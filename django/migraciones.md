Creamos la app ks:

    ./manage.py startapp ks

Añadimos a las apps que viene por defecto nuestra ueva app, 
ks, añadiendlo a la lista `INSTALLED_APPS`. Debe quedar algo así:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'ks',
    ]

Creamos nuestro modelo para el proyecto. Como no
tenemos todavía claros los atributos que tiene el proyecto, crearemos
una modelo con lo mínimo, un identificador para el proyecto 
y un título:

    from django.db import models

    # Create your models here.

    class Project(models.Model):
        id_project = models.AutoField(primary_key=True)
        title = models.CharField(max_length=230)

Ya tenemos el primer cambio en la base de datos. Hay una nueva tabla que
servirá para almacenar la información de los proyectos. Podemos crear y 
mantener actualizadas las tablas en la basa de datos con respecto a nuestros
modelos mediante un sistema incluido en Django desde la versión 1.7
llamado **migraciones** (_migratons_).

Con este sistema, todo cambio en la base de datos (añadir un campo, borrar un
modelo, etc) se raliza mediante migraciones. Una migración es un conjunto de uno
o más cambios.  En nuestro caso, la migracion sera el paso de no tener ninguna
tabla a tener la tabla creada con los dos campos indicados.

El porcedimiento par realizar un cambio en la base de datos sería tal y 
como sigue:

1) realizamos los cambios en el modelo. Se recomienda realizar muchos cambios
pequeños, en ves de pocos cambios muy grandes, para poder mantener un mejor
control y una mejor comprensión de los cambios realizados

2) generamos las migraciones con el comando `makemigrations`

3) opcionalmente, podemos ver todos los cambios, estén alpicados o 
   no, con el comando `showmigrations`

4) Finalmente, aplicaremos los cambios con el comando `migrate`

La información de que migraciones se han aplicado a la base de datos se guarda
internamente en la propia base de datos, así que si ejecutamos `migrate` solo
se aplicarán las migraciones que están pendientes, nunca se aplican dos veces
la misma migración. Dicho en otras palabras, podemos ejecutar el 
comando `migrate` todas las veces que queramos, es _idempotente_.

Si vamos ahora al admin, veremos que nuestro modelo no aparece. Para poder 
gestionar nuestro projectos con al admin, tenemos que abrir el fichero
`admin.py` de nuestro app y añadir dos líneas:

    from . import models 

    admin.site.register(models.project)

Si recargamos la vista del admin vemos que ya podemos 
gestionar de forma básica nuestro modelo: podemos
crear nuevos proyectos, editar, borrar. A modo 
de ejercicio, creemos un priyecto nuevo y luego lo 
borraremos.

Vemos que el proyecto se lista con una descripción genérica,
`Project object`. Es porque no hemos definido en nuestro 
modelo como debe representarse a si mismo como string. Para 
ello podemos definir el método `__str__` en la clase, que 
debe retornar una string. Añadamos este método a la clase `Project`:

    def __str__(self):
        return 'Projecto {}: {}'.format(
            self.id_proyecto, self.title
            )

Si recargamos la página del admin, vemos que el listado ya 
refleja estos cambios.

Vamos a añadir al modelo proyecto un par de campos más: 

 - La fecha límite para el proyecto. Si en esa fecha no se ha alcanzado
   la meta, el proyecto se descartará como fallido.

 - La cantidad de dinero nedesaria para que el proyecto se financia.

Para ello modificamos la clase añadiendo esos dos campos, que llamaremos
_deadline_ y _target_:

    class Project(models.Model):
    
    id_project = models.AutoField(primary_key=True)
    title = models.CharField(max_length=230)
    deadline = models.DateField()
    target = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return 'Proyecto {}: {}'.format(
            self.id_project, self.title
            )

Hemos modificado el modelo, asi que la tabla en la base de datos no 
coincide con el modelo, hay que realizar una migración. Los pasos
son los de siempre:

1) hacer un `check` para ver si todo esta correcto sintácticamente
2) hacer un `makemigrations`
3) hacer un 'migrate'

Pero al hacer el ``makemigrations`, nos sale un aviso:

    You are trying to add a non-nullable field 'deadline' to project
    without a default; we can't do that (the database needs something 
    to populate existing rows).
    Please select a fix:
     1) Provide a one-off default now (will be set on all existing 
        rows with a null value for this column)
     2) Quit, and let me add a default in models.py
    Select an option:

El problema viene de que hemos añadido un campo que por defecto no puede 
ser nulo, y no queda claro que hacer en el caso de que ya existieran registros
en la tabla. nos ofrece dos alternaticas para resolver la ambigüedad, o bien
proporcinar un valor por defecto de forma interactiva, o bien dandonos
la oportunidad de añadir un valor por defecto. Vamos a salir, pero en 
vez de añadir un valor por defecto, modificaremos el campo `deadline` 
para que acepte valores nulo, y que ese será el valor por defecto. También 
nos haría lo mismo para el campo `limit`, asi que le asignamos
tambien un valor por defecto:

    class Project(models.Model):
        
        id_project = models.AutoField(primary_key=True)
        title = models.CharField(max_length=230)
        deadline = models.DateField(blank=True, default=None)
        limit = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)

        def __str__(self):
            return 'Proyecto {}: {}'.format(
                self.id_project, self.title
                )

Ahora si podemos hacer la secuencia `check`, `makemigrations` y `migrate`. El 
resultado debería ser algo así:

    Migrations for 'ks':
      ks/migrations/0002_auto_20171031_1949.py
        - Add field deadline to project
        - Add field limit to project
