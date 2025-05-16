import os
import cv2
import numpy as np
import requests
from io import BytesIO
from urllib.parse import urlparse

class ImageUtils:
    """
    Clase con utilidades para manejar imágenes:
    - Leer imágenes locales
    - Leer imágenes desde URL
    - Guardar imágenes en el sistema local
    """
    
    @staticmethod
    def read_image_from_path(image_path):
        """
        Lee una imagen desde una ruta local
        
        Args:
            image_path (str): Ruta a la imagen local
            
        Returns:
            numpy.ndarray: Array de la imagen
            str: Nombre de archivo de la imagen
        """
        try:
            # Comprobar si el archivo existe
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"No se encontró la imagen en: {image_path}")
            
            # Leer la imagen con OpenCV
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"No se pudo cargar la imagen desde {image_path}")
            
            # Obtener el nombre del archivo
            filename = os.path.basename(image_path)
            
            return img, filename
        except Exception as e:
            print(f"Error al leer la imagen local: {str(e)}")
            raise
    
    @staticmethod
    def read_image_from_url(image_url):
        """
        Lee una imagen desde una URL
        
        Args:
            image_url (str): URL de la imagen
            
        Returns:
            numpy.ndarray: Array de la imagen
            str: Nombre de archivo de la imagen
        """
        try:
            # Obtener el nombre del archivo de la URL
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path)
            
            # Descargar la imagen
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Lanzar excepción si hay error HTTP
            
            # Convertir a array NumPy
            image_data = BytesIO(response.content)
            img_array = np.asarray(bytearray(image_data.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError(f"No se pudo decodificar la imagen desde {image_url}")
            
            return img, filename
        except Exception as e:
            print(f"Error al leer la imagen desde URL: {str(e)}")
            raise
    
    @staticmethod
    def save_image(img, save_path):
        """
        Guarda una imagen en una ruta específica
        
        Args:
            img (numpy.ndarray): Array de la imagen a guardar
            save_path (str): Ruta donde guardar la imagen
            
        Returns:
            str: Ruta completa donde se guardó la imagen
        """
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Guardar la imagen
            result = cv2.imwrite(save_path, img)
            if not result:
                raise IOError(f"No se pudo guardar la imagen en {save_path}")
            
            return save_path
        except Exception as e:
            print(f"Error al guardar la imagen: {str(e)}")
            raise
    
    @staticmethod
    def ensure_directory_exists(directory):
        """
        Asegura que un directorio exista, creándolo si es necesario
        
        Args:
            directory (str): Ruta del directorio
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

# Ejemplo de uso
if __name__ == "__main__":
    # Por ejemplo:
    # img, filename = ImageUtils.read_image_from_path("ruta/a/imagen.jpg")
    # ImageUtils.save_image(img, "ruta/salida/imagen_guardada.jpg")
    pass