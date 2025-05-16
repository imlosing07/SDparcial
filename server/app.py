import os
from flask import Flask, request, render_template, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
import uuid
import cv2
import numpy as np

app = Flask(__name__)

# Configuración para carga y almacenamiento de archivos
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
PROCESSED_FOLDER = os.path.join(app.root_path, 'static', 'processed')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Crear directorios si no existen
for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Límite 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.lower().split('.')[-1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Obtener lista de imágenes disponibles en el servidor
    server_images = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            image_url = url_for('static', filename=f'uploads/{filename}')
            server_images.append({'name': filename, 'url': image_url})
    
    # Obtener lista de imágenes procesadas
    processed_images = []
    for filename in os.listdir(PROCESSED_FOLDER):
        if allowed_file(filename):
            image_url = url_for('static', filename=f'processed/{filename}')
            processed_images.append({'name': filename, 'url': image_url})
    
    return render_template('index.html', 
                          server_images=server_images,
                          processed_images=processed_images)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verificar si la solicitud tiene un archivo
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró ningún archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if file and allowed_file(file.filename):
        # Generar un nombre de archivo seguro y único
        original_filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4().hex}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Devolver la URL de la imagen cargada
        image_url = url_for('static', filename=f'uploads/{filename}')
        return jsonify({
            'message': 'Imagen cargada correctamente',
            'filename': filename,
            'url': image_url
        })
    
    return jsonify({'error': 'Tipo de archivo no permitido'}), 400

@app.route('/save_processed', methods=['POST'])
def save_processed():
    # Verificar si la solicitud tiene un archivo
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró ningún archivo procesado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if file and allowed_file(file.filename):
        # Generar un nombre de archivo único para la imagen procesada
        original_filename = secure_filename(file.filename)
        # Añadir prefijo para identificar que es una imagen procesada
        if not original_filename.startswith('otsu_'):
            filename = f"otsu_{original_filename}"
        else:
            filename = original_filename
            
        filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        file.save(filepath)
        
        # Devolver la URL de la imagen procesada
        image_url = url_for('static', filename=f'processed/{filename}')
        return jsonify({
            'message': 'Imagen procesada guardada correctamente',
            'filename': filename,
            'url': image_url
        })
    
    return jsonify({'error': 'Tipo de archivo no permitido'}), 400

@app.route('/processed', methods=['POST'])
def processed():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró ningún archivo'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        processed_filename = f"otsu_{original_filename}"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)

        # Leer imagen desde el archivo directamente (sin guardarla)
        file_bytes = file.read()
        np_array = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'No se pudo leer la imagen'}), 400

        # Aplicar algoritmo Otsu
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, otsu_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Guardar resultado directamente en PROCESSED_FOLDER
        cv2.imwrite(output_path, otsu_img)

        # Retornar resultado
        image_url = url_for('static', filename=f'processed/{processed_filename}')
        return jsonify({
            'message': 'Imagen procesada guardada correctamente',
            'filename': processed_filename,
            'url': image_url
        })

    return jsonify({'error': 'Tipo de archivo no permitido'}), 400


@app.route('/images')
def list_images():
    """Endpoint para listar todas las imágenes disponibles en el servidor"""
    images = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            image_url = url_for('static', filename=f'uploads/{filename}')
            images.append({'name': filename, 'url': image_url})
    
    return jsonify(images)

@app.route('/image/<filename>')
def get_image(filename):
    """Endpoint para obtener una imagen específica del servidor"""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')