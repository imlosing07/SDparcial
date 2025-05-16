import cv2
import numpy as np
import os

class OtsuProcessor:
    """
    Clase que implementa el algoritmo de umbralización de Otsu para
    segmentación de imágenes en blanco y negro.
    """
    
    def __init__(self):
        """Inicializa el procesador Otsu"""
        pass
        
    def apply_otsu(self, image_path, save_path=None):
        """
        Aplica el algoritmo de Otsu a una imagen
        
        Args:
            image_path (str): Ruta a la imagen de entrada
            save_path (str, optional): Ruta donde guardar la imagen procesada.
                                     Si es None, la imagen no se guarda.
        
        Returns:
            numpy.ndarray: Imagen procesada con algoritmo Otsu
            str: Ruta donde se guardó la imagen (si save_path no es None)
        """
        try:
            # Leer la imagen
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"No se pudo cargar la imagen desde {image_path}")
            
            # Convertir a escala de grises si no lo está
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
                
            # Aplicar umbralización de Otsu
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Si se especificó una ruta para guardar, guardar la imagen
            if save_path:
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                cv2.imwrite(save_path, thresh)
                return thresh, save_path
            
            return thresh, None
            
        except Exception as e:
            print(f"Error al procesar la imagen con Otsu: {str(e)}")
            raise
    
    def apply_otsu_from_array(self, img_array, save_path=None):
        """
        Aplica el algoritmo de Otsu a un array NumPy (imagen en memoria)
        
        Args:
            img_array (numpy.ndarray): Array de la imagen
            save_path (str, optional): Ruta donde guardar la imagen procesada
        
        Returns:
            numpy.ndarray: Imagen procesada con algoritmo Otsu
            str: Ruta donde se guardó la imagen (si save_path no es None)
        """
        try:
            # Convertir a escala de grises si no lo está
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = img_array
                
            # Aplicar umbralización de Otsu
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Si se especificó una ruta para guardar, guardar la imagen
            if save_path:
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                cv2.imwrite(save_path, thresh)
                return thresh, save_path
            
            return thresh, None
            
        except Exception as e:
            print(f"Error al procesar la imagen con Otsu: {str(e)}")
            raise

# Ejemplo de uso
if __name__ == "__main__":
    processor = OtsuProcessor()
    # Ejemplo: processor.apply_otsu("ruta/a/imagen.jpg", "ruta/salida/imagen_otsu.jpg")