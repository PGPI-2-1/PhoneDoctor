Existen tres formas de desplegar la aplicación: En local, mediante docker, o accediendo al proyecto ya desplegado en Python Anywhere.

1.	Local:
Para desplegar la aplicación en local debemos clonar el repositorio en nuestro PC desde el enlace de github: https://github.com/PGPI-2-1/PhoneDoctor.git, o mediante el zip entregado en Enseñanza Virtual
Una vez lo tengamos descargado, realizamos los siguientes comandos:

pip install -r requirements

python manage.py migrate
python manage.py loaddata populate.json (para crear algunos datos iniciales)
python manage.py runserver

En caso de que de problemas por la base de datos, antes de hacer la migración:
Eliminamos el archivo db.sqlite3 y hacemos los siguientes comandos:
python manage.py flush
python manage.py makemigrations

2.	Docker:
Para ejecutar la imagen de docker, debemos descargar el archivo .tar entregado por Enseñanza Virtual. Después, ejecutamos los siguientes comandos estando en el directorio donde está el archivo descargado:

docker load -i phonedoctorDocker.tar
docker run -p 8080:8000 docker/phonedoctor-g2-1:latest python manage.py runserver 
0.0.0.0: 8000
En caso de que de error por los puertos, debemos cambiar el 8080 por el puerto que tengamos libre

3.	Python Anywhere:
Para acceder a la aplicación ya desplegada, simplemente entramos en:
https://pphonedoctor.eu.pythonanywhere.com/
