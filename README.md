# Ejecutar la api
En consola, dentro del enviroment, ejecutar:
```shell
flask run
```
este comando buscara un archivo llamado `app.py` y dentro de este una variable llamada `app` que contiene el metodo `run()`, ademas, si existe el archivo `.flaskenv` usara esos valores en conjunto la libreria `python-dotenv` para ejecutar la app, esto sustituye si se ejecuta el archivo directamente en vez de por contenedores


# Manipulacion enviroment
1. Para empezar el enviroment, en consola
```shell
py -m venv .venv
```
2. Para abrir el enviroment, en consola
```shell
.\.venv\Scripts\activate
```
3. Para cerrar el enviroment
```shell
deactivate
```
4. Para generar requirements.txt
```shell
pip freeze > requirements.txt
```
5. Para instalar todo requirements.txt
```shell
pip install -r requirements.txt
```

# Manipulacion container
1. Crear en carpeta un archivo llamado "Dockerfile"
2. Crear la imagen necesaria
3. Ejecutar en consola
```shell
docker build -t rest-apis-flask-python-personal-training .
```
4. Para actualizar la imagen se ejecuta:
```shell
docker build -t rest-apis-flask-python-personal-training .
```
5. Para ejecutar el contenedor, se escoge un puerto, por ejemplo el 5005 y se ejecuta:
```shell
docker run -p 5005:5000
```
6. Para ejecutar el contenedor en segundo plano y liberar la consola se ejecuta:
```shell
docker run -dp 5005:5000
```
7. Crear el documento docker-compose.yml para juntar otros contenedores, por ejemplo el contenedor de la base de datos e inicializarlos juntos
8. Correr el compose
```shell
docker compose up
```
9. Para correr y que se actualice mientras se esta en desarollo en windows
```shell
docker run -dp 5005:5000 -w /app -v "c:/app" rest-apis-flask-python-personal-training
```


# Teoria API
- **recurso:** URI's para acceder a la manipulacion o lectura de nuestra API, en este ejemplo seria `/users`
- **endpoint:** la URL completa `http://127.0.0.1:5000/users`

- Los recursos deben ser _sustantivos_ y deben estar en _plural_
- Se recomienda una arquitectura por capas
- **asociacion:** Cuando se quieren juntar dos recursos, por  ejemplo, todos los documentos del usuario 4 `http://127.0.0.1:5000/users/4/documents` y asi sucesivamente, si se quiere manipular el documento 10 del usuario 4 `http://127.0.0.1:5000/users/4/documents/10`
- **request:** Peticion del cliente al api a traves del protocolo http y se compone de:
  - **header:** Metadata, cookies, cabeceras, etc.
  - **body:** Informacion relevante conmunmente en formato JSON
  - **queryString:** Informacion que forma parte de la URL como parametros seguida del signo `?`, por ejemplo: `127.0.0.1:5000/users?orderBy=creationDate`, se paso la variable _orderBy_ con el valor _creationDate_
- **response:** Respuesta de la api al cliente, cada request tiene su response y se compone de:
  - **header:** Metadata
  - **Body:** Informacion relevante en formato comunmente JSON
  - **status code:** codigos estandar de respuestas cliente-servidor
    - **400 - Bad Request** Informacion del cliente no puede ser interpretada
    - **401 - Unauthorized** Acceso no autorizado
    - **403 - Forbidden** Acceso autorizado pero sin permisos necesarios
    - **404 - Not Found** Recurso no se encuentra, no autorizado
    - **500 - Internal Server Error** Excepciones no controladas
    - **504 - Gateway Timeout** No pudo responder a tiempo la peticion
- **stateless:** Un principio de diseño, las apis no persisten informacion entre un request y un response tales como cookies o variables de sesion
- **cacheable:** Principío de diseño para mejorar el rendimiento, se puede cachear la respuesta del servidor, los mecanismos mas usados son
  - **REDIS**
  - **MEMCACHE**
- **swagger:** Serie de reglas para documentar una API, es un paquete externo que automatiza la documentacion
- **autenticacion:** Proceso por el cual un cliente se identifica ante una API, un mecanismo puede ser los `JWT` (JSON Web Token)
- **autorizacion:** Permisos que tienen los clientes, un mecanismo puede ser la asignacion de roles
- **JWT:** El proceso es basico, Primero el usuario se autentica en el sistema con sus credenciales; Si las credenciales son correctas, el sistema responde un token; los tokens se envian en el _header_ y contiene:
  - Tiempo de expiracion (si o si)
  - id del cliente (si o si)
  - otra informacion relevante (tambien conocida como _claims_)
  

### Estandar para acceder a los recursos CRUD de un API

| Operacion | Metodo | Endpoint |  Observacion |
| :-: | :-: | :-: | :---: |
| get all | GET | `127.0.0.1:5000/users` | - |
| get one | GET | `127.0.0.1:5000/users/4` | - |
| create | POST | `127.0.0.1:5000/users` | - |
| update | PUT | `127.0.0.1:5000/users/4` | Si el usuario 4 no existe, lo crea,  ademas, deben ir todos los datos o se generaran campos null |
| delete | DELETE | `127.0.0.1:5000/users/4` | - |
| update parcial | PATCH | `127.0.0.1:5000/users/4` | Los campos vacios no los llena de null |
| - | HEAD | `127.0.0.1:5000/users` | Peticion sin body ni queryString |
| - | CONNECT | `127.0.0.1:5000/users` | Establece un túnel hacia el servidor identificado por el recurso |
| - | OPTIONS | `127.0.0.1:5000/users/4` | Para describir las opciones de comunicación con el recurso de destino |
| - | TRACE | `127.0.0.1:5000/users/4` | Realiza una prueba de bucle de retorno de mensaje a lo largo de la ruta al recurso de destino |


### Operaciones dentro de una API
operaciones tales como `ordenamiento`, `filtrado`, `busqueda` y `paginacion` deberian ir por queryStrings en vez de crear endpoints adicionales

#### Ordenamiento
Ejemplos:
- `/users?sort_by=firstName`
- `/users?sort_by=firstName:desc`

#### Filtrado
Ejemplos:
- `/users?userId=1,2,3`

#### Filtrado
Ejemplos:
- `/users?search=eduardo rodriguez`
- 
#### Paginacion
Se recomienda en el cuerpo de la respuesta agregar informacion como la pagina actual, las paginas totales y el total de registros
- `/users?limit=20` de 20 en 20
- `/users?page=1&take=20` de la pagina 1 tomar 20 valores

### Errores 