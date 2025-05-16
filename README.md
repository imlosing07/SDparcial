Sistema Distribuido Cliente-Servidor con Algoritmo Otsu
Este proyecto implementa un sistema distribuido con arquitectura cliente-servidor para el procesamiento de imágenes utilizando el algoritmo de Otsu. El servidor está desarrollado con Flask y proporciona una interfaz web, mientras que el cliente está implementado en Python puro.

Estructura del Proyecto
/sistemas-distribuidos
├── server/
│   ├── static/               # Archivos de imagen
│   │   ├── uploads/          # Imágenes subidas por el usuario
│   │   └── processed/        # Imágenes procesadas con Otsu
│   ├── templates/            # HTMLs (index.html)
│   ├── app.py                # Servidor Flask
│   └── requirements.txt      # Dependencias del servidor
├── client/
│   ├── otsu_processor.py     # Aplica el algoritmo Otsu
│   ├── image_utils.py        # Funciones auxiliares (leer, guardar imágenes)
│   ├── send_to_server.py     # Lógica de envío/descarga entre cliente-servidor
│   ├── client.py             # Interfaz principal del cliente
│   └── requirements.txt      # Dependencias del cliente
└── README.md                 # Este archivo
Funcionalidad Principal
El sistema implementa los siguientes casos de uso:

Caso 1: Leer una imagen desde el servidor, procesarla aplicando el algoritmo de Otsu en el cliente y luego enviarla de vuelta al servidor.
Caso 2: Leer una imagen desde el cliente, procesarla aplicando el algoritmo de Otsu y enviarla al servidor.
Caso 3: Leer una imagen desde el servidor, procesarla en el cliente aplicando el algoritmo de Otsu y guardarla localmente en el cliente.
Instalación
Servidor
Navega al directorio del servidor:
bash
cd server
Instala las dependencias:
bash
pip install -r requirements.txt
Ejecuta el servidor:
bash
python app.py
El servidor estará disponible en http://localhost:5000
Cliente
Navega al directorio del cliente:
bash
cd client
Instala las dependencias:
bash
pip install -r requirements.txt
Ejecuta el cliente:
bash
python client.py --server http://localhost:5000
Uso del Cliente
El cliente proporciona una interfaz por consola con las siguientes opciones:

Obtener imágenes del servidor: Muestra la lista de imágenes disponibles en el servidor.
Procesar imagen del servidor y guardarla en el servidor (Caso 1): Selecciona una imagen del servidor, la procesa con Otsu y la envía de vuelta al servidor.
Procesar imagen local y enviarla al servidor (Caso 2): Selecciona una imagen local, la procesa con Otsu y la envía al servidor.
Procesar imagen del servidor y guardarla localmente (Caso 3): Selecciona una imagen del servidor, la procesa con Otsu y la guarda localmente.
Configurar servidor: Cambia la URL del servidor.
Abrir interfaz web: Abre la interfaz web del servidor en el navegador.
También se puede utilizar el cliente con argumentos desde la línea de comandos:

bash
# Procesar imagen del servidor y guardarla en el servidor (Caso 1)
python send_to_server.py --server http://localhost:5000 --mode server-to-server --image imagen.jpg

# Procesar imagen local y enviarla al servidor (Caso 2)
python send_to_server.py --server http://localhost:5000 --mode client-to-server --image /ruta/a/imagen.jpg

# Procesar imagen del servidor y guardarla localmente (Caso 3)
python send_to_server.py --server http://localhost:5000 --mode server-to-client --image imagen.jpg
Interfaz Web
El servidor proporciona una interfaz web accesible desde http://localhost:5000 con las siguientes funcionalidades:

Subir imágenes al servidor
Ver y seleccionar imágenes del servidor para procesarlas
Procesar imágenes locales y enviarlas al servidor
Ver las imágenes procesadas
Algoritmo de Otsu
El algoritmo de Otsu es una técnica de umbralización automática que se utiliza para la binarización de imágenes. Calcula el umbral óptimo para separar los píxeles de una imagen en dos clases (primer plano y fondo), minimizando la varianza intraclase.

En este proyecto, el algoritmo se implementa utilizando OpenCV en la clase OtsuProcessor.

Despliegue en PythonAnywhere
Para desplegar el servidor en PythonAnywhere, sigue estos pasos:

Crea una cuenta en PythonAnywhere (https://www.pythonanywhere.com/).
Sube los archivos del servidor a PythonAnywhere:
Utiliza la sección "Files" para crear los directorios necesarios
Sube manualmente los archivos o utiliza Git
Crea un nuevo Web App en PythonAnywhere:
Selecciona "Web" en el panel de control
Haz clic en "Add a new web app"
Selecciona "Flask" y la versión de Python adecuada
Configura la ruta a tu aplicación (app.py)
Configura el archivo WSGI:
python
import sys

# Añadir el directorio de la aplicación al path
path = '/home/tuusuario/ruta/a/tu/app'
if path not in sys.path:
    sys.path.append(path)

# Importar la aplicación Flask
from app import app as application
Configura los directorios estáticos en la sección de configuración de la aplicación web:
URL: /static/
Directorio: /home/tuusuario/ruta/a/tu/app/static
Instala las dependencias utilizando la consola de PythonAnywhere:
bash
pip3 install --user -r requirements.txt
Reinicia la aplicación web desde el panel de control.
Una vez desplegado, podrás acceder a tu aplicación en https://tuusuario.pythonanywhere.com

Notas importantes para PythonAnywhere
Asegúrate de que las rutas en app.py sean relativas y no absolutas.
PythonAnywhere tiene restricciones de acceso a sitios externos en cuentas gratuitas, lo que puede afectar a la funcionalidad de comunicación con clientes externos.
La carpeta static debe ser accesible para guardar las imágenes subidas y procesadas.
Licencia
Este proyecto está disponible como código abierto bajo los términos de la licencia MIT.

