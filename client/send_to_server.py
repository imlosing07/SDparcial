import os
import requests
import argparse
import time
from io import BytesIO
import tempfile
from urllib.parse import urljoin
import cv2

from otsu_processor import OtsuProcessor
from image_utils import ImageUtils

class ClientServer:
    """
    Clase que maneja la comunicación entre el cliente y el servidor.
    Implementa la lógica para los diferentes casos de uso:
    1. Leer imagen del servidor, procesarla en el cliente y enviarla al servidor
    2. Leer imagen del cliente, procesarla y enviarla al servidor
    3. Leer imagen del servidor, procesarla en el cliente y guardarla localmente
    """
    
    def __init__(self, server_url):
        """
        Inicializa el cliente con la URL del servidor
        
        Args:
            server_url (str): URL base del servidor (ej: http://localhost:5000 o https://usuario.pythonanywhere.com)
        """
        self.server_url = server_url.rstrip('/')
        self.processor = OtsuProcessor()
        
        # Crear directorio para guardar imágenes procesadas localmente
        self.local_output_dir = os.path.join(os.getcwd(), 'processed_images')
        ImageUtils.ensure_directory_exists(self.local_output_dir)
    
    def get_server_images(self):
        """
        Obtiene la lista de imágenes disponibles en el servidor
        
        Returns:
            list: Lista de diccionarios con información de las imágenes
        """
        try:
            response = requests.get(f"{self.server_url}/images")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al obtener imágenes del servidor: {str(e)}")
            return []
    
    def case1_server_to_server(self, image_url, image_name):
        """
        CASO 1: Procesa una imagen del servidor y guarda el resultado en el servidor
        
        Args:
            image_url (str): URL de la imagen en el servidor
            image_name (str): Nombre de la imagen
            
        Returns:
            dict: Respuesta del servidor con la URL de la imagen procesada
        """
        try:
            print(f"Procesando imagen del servidor: {image_name}")
            
            # CORRECCIÓN: Asegurarse de que la URL sea absoluta
            if image_url.startswith('/'):
                full_image_url = urljoin(self.server_url, image_url)
            else:
                full_image_url = image_url
                
            print(f"URL completa de la imagen: {full_image_url}")
            
            # 1. Descargar la imagen del servidor
            img, _ = ImageUtils.read_image_from_url(full_image_url)
            
            # 2. Guardar temporalmente para procesar con Otsu
            temp_dir = tempfile.gettempdir()
            temp_input_path = os.path.join(temp_dir, image_name)
            cv2.imwrite(temp_input_path, img)
            
            # 3. Procesar con algoritmo Otsu
            temp_output_path = os.path.join(temp_dir, f"otsu_{image_name}")
            processed_img, _ = self.processor.apply_otsu(temp_input_path, temp_output_path)
            
            print(f"Imagen procesada con Otsu guardada temporalmente en: {temp_output_path}")
            
            # 4. Enviar la imagen procesada al servidor
            with open(temp_output_path, 'rb') as f:
                files = {'file': (f"otsu_{image_name}", f, 'image/jpeg')}
                response = requests.post(f"{self.server_url}/save_processed", files=files)
                response.raise_for_status()
            
            # 5. Limpiar archivos temporales
            os.remove(temp_input_path)
            os.remove(temp_output_path)
            
            result = response.json()
            print(f"Imagen procesada subida al servidor: {result['url']}")
            return result
            
        except Exception as e:
            print(f"Error en case1_server_to_server: {str(e)}")
            raise
    
    def case2_client_to_server(self, local_image_path):
        """
        CASO 2: Procesa una imagen local y guarda el resultado en el servidor
        
        Args:
            local_image_path (str): Ruta a la imagen local
            
        Returns:
            dict: Respuesta del servidor con la URL de la imagen procesada
        """
        try:
            print(f"Procesando imagen local: {local_image_path}")
            
            # 1. Verificar que la imagen existe
            if not os.path.exists(local_image_path):
                raise FileNotFoundError(f"No se encontró la imagen en: {local_image_path}")
            
            # 2. Procesar con algoritmo Otsu
            filename = os.path.basename(local_image_path)
            temp_dir = tempfile.gettempdir()
            temp_output_path = os.path.join(temp_dir, f"otsu_{filename}")
            processed_img, _ = self.processor.apply_otsu(local_image_path, temp_output_path)
            
            print(f"Imagen procesada con Otsu guardada temporalmente en: {temp_output_path}")
            
            # 3. Enviar la imagen procesada al servidor
            with open(temp_output_path, 'rb') as f:
                files = {'file': (f"otsu_{filename}", f, 'image/jpeg')}
                response = requests.post(f"{self.server_url}/save_processed", files=files)
                response.raise_for_status()
            
            # 4. Limpiar archivos temporales
            os.remove(temp_output_path)
            
            result = response.json()
            print(f"Imagen procesada subida al servidor: {result['url']}")
            return result
            
        except Exception as e:
            print(f"Error en case2_client_to_server: {str(e)}")
            raise
    
    def case3_server_to_client(self, image_url, image_name):
        """
        CASO 3: Procesa una imagen del servidor y guarda el resultado en el cliente (localmente)
        
        Args:
            image_url (str): URL de la imagen en el servidor
            image_name (str): Nombre de la imagen
            
        Returns:
            str: Ruta local donde se guardó la imagen procesada
        """
        try:
            print(f"Procesando imagen del servidor para guardar localmente: {image_name}")
            
            # CORRECCIÓN: Asegurarse de que la URL sea absoluta
            if image_url.startswith('/'):
                full_image_url = urljoin(self.server_url, image_url)
            else:
                full_image_url = image_url
                
            print(f"URL completa de la imagen: {full_image_url}")
            
            # 1. Descargar la imagen del servidor
            img, _ = ImageUtils.read_image_from_url(full_image_url)
            
            # 2. Guardar temporalmente para procesar con Otsu
            temp_dir = tempfile.gettempdir()
            temp_input_path = os.path.join(temp_dir, image_name)
            cv2.imwrite(temp_input_path, img)
            
            # 3. Procesar con algoritmo Otsu
            local_output_path = os.path.join(self.local_output_dir, f"otsu_{image_name}")
            processed_img, saved_path = self.processor.apply_otsu(temp_input_path, local_output_path)
            
            # 4. Limpiar archivos temporales
            os.remove(temp_input_path)
            
            print(f"Imagen procesada con Otsu guardada localmente en: {saved_path}")
            return saved_path
            
        except Exception as e:
            print(f"Error en case3_server_to_client: {str(e)}")
            raise
    
    def process_both_ways(self, image_url, image_name, save_local=True, save_server=True):
        """
        Procesa una imagen y la guarda tanto localmente como en el servidor, según las opciones
        
        Args:
            image_url (str): URL de la imagen en el servidor
            image_name (str): Nombre de la imagen
            save_local (bool): Si es True, guarda la imagen localmente
            save_server (bool): Si es True, guarda la imagen en el servidor
            
        Returns:
            dict: Información sobre las rutas donde se guardó la imagen
        """
        result = {
            "local_path": None,
            "server_response": None
        }
        
        # CORRECCIÓN: Asegurarse de que la URL sea absoluta
        if image_url.startswith('/'):
            full_image_url = urljoin(self.server_url, image_url)
        else:
            full_image_url = image_url
        
        # 1. Descargar la imagen del servidor
        img, _ = ImageUtils.read_image_from_url(full_image_url)
        
        # 2. Guardar temporalmente para procesar con Otsu
        temp_dir = tempfile.gettempdir()
        temp_input_path = os.path.join(temp_dir, image_name)
        cv2.imwrite(temp_input_path, img)
        
        # 3. Procesar con algoritmo Otsu
        temp_output_path = os.path.join(temp_dir, f"otsu_{image_name}")
        processed_img, _ = self.processor.apply_otsu(temp_input_path, temp_output_path)
        
        # 4. Guardar según opciones
        if save_local:
            local_output_path = os.path.join(self.local_output_dir, f"otsu_{image_name}")
            ImageUtils.save_image(processed_img, local_output_path)
            result["local_path"] = local_output_path
            print(f"Imagen guardada localmente en: {local_output_path}")
        
        if save_server:
            with open(temp_output_path, 'rb') as f:
                files = {'file': (f"otsu_{image_name}", f, 'image/jpeg')}
                response = requests.post(f"{self.server_url}/save_processed", files=files)
                response.raise_for_status()
                result["server_response"] = response.json()
                print(f"Imagen subida al servidor: {response.json()['url']}")
        
        # 5. Limpiar archivos temporales
        os.remove(temp_input_path)
        os.remove(temp_output_path)
        
        return result

def main():
    """Función principal para ejecutar el cliente desde línea de comandos"""
    
    parser = argparse.ArgumentParser(description='Cliente para procesamiento de imágenes con algoritmo Otsu')
    parser.add_argument('--server', required=True, help='URL del servidor (ej: http://localhost:5000)')
    parser.add_argument('--mode', required=True, choices=['server-to-server', 'client-to-server', 'server-to-client'],
                        help='Modo de operación')
    parser.add_argument('--image', required=True, 
                        help='Ruta a imagen local (para client-to-server) o nombre de imagen en servidor (para otros modos)')
    
    args = parser.parse_args()
    
    client = ClientServer(args.server)
    
    if args.mode == 'server-to-server':
        # Buscar la imagen en el servidor
        server_images = client.get_server_images()
        image_url = None
        for img in server_images:
            if args.image in img['name']:
                image_url = img['url']
                break
        
        if not image_url:
            print(f"Error: No se encontró la imagen '{args.image}' en el servidor")
            return
        
        client.case1_server_to_server(image_url, args.image)
        
    elif args.mode == 'client-to-server':
        client.case2_client_to_server(args.image)
        
    elif args.mode == 'server-to-client':
        # Buscar la imagen en el servidor
        server_images = client.get_server_images()
        image_url = None
        for img in server_images:
            if args.image in img['name']:
                image_url = img['url']
                break
        
        if not image_url:
            print(f"Error: No se encontró la imagen '{args.image}' en el servidor")
            return
        
        client.case3_server_to_client(image_url, args.image)

if __name__ == "__main__":
    main()