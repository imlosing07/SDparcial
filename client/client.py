import os
import sys
import argparse
import json
import webbrowser
from send_to_server import ClientServer

def print_header(text):
    """Imprime un encabezado con formato"""
    print("\033[2J\033[H")
    print(f" {text}")
    print("=" * 60)

def main():
    """Interfaz principal del cliente para procesamiento de imágenes"""
    
    parser = argparse.ArgumentParser(description='Cliente para Sistema Distribuido con Algoritmo Otsu')
    parser.add_argument('--server', default='http://localhost:5000', 
                        help='URL del servidor (ej: http://localhost:5000 o https://usuario.pythonanywhere.com)')
    parser.add_argument('--open-browser', action='store_true',
                        help='Abrir el navegador con la interfaz web del servidor')

    args = parser.parse_args()
    
    # Inicializar el cliente
    client = ClientServer(args.server)
    
    # Abrir navegador si se solicitó
    if args.open_browser:
        webbrowser.open(args.server)
    
    while True:
        print_header("SISTEMA DISTRIBUIDO - CLIENTE OTSU")
        print(f"Servidor conectado: {args.server}")
        print("\nOpciones disponibles:")
        print("1. Obtener imágenes del servidor")
        print("2. Procesar imagen del servidor y guardarla en el servidor (Caso 1)")
        print("3. Procesar imagen local y enviarla al servidor (Caso 2)")
        print("4. Procesar imagen del servidor y guardarla localmente (Caso 3)")
        print("5. Configurar servidor")
        print("6. Abrir interfaz web")
        print("0. Salir")
        
        choice = input("\nSeleccione una opción: ")
        
        if choice == '0':
            print("¡Hasta pronto!")
            break
        
        elif choice == '1':
            print_header("IMÁGENES DISPONIBLES EN EL SERVIDOR")
            try:
                images = client.get_server_images()
                if not images:
                    print("No hay imágenes disponibles en el servidor")
                else:
                    print(f"Se encontraron {len(images)} imágenes:")
                    for i, img in enumerate(images):
                        print(f"[{i+1}] {img['name']} - {img['url']}")
            except Exception as e:
                print(f"Error al obtener imágenes: {str(e)}")
            
            input("\nPresione Enter para continuar...")
        
        elif choice == '2':
            print_header("PROCESAR IMAGEN DEL SERVIDOR (CASO 1)")
            try:
                images = client.get_server_images()
                if not images:
                    print("No hay imágenes disponibles en el servidor")
                else:
                    print("Imágenes disponibles:")
                    for i, img in enumerate(images):
                        print(f"[{i+1}] {img['name']}")
                    
                    idx = int(input("\nSeleccione el número de imagen a procesar: ")) - 1
                    if 0 <= idx < len(images):
                        selected_img = images[idx]
                        print(f"\nProcesando {selected_img['name']}...")
                        result = client.case1_server_to_server(selected_img['url'], selected_img['name'])
                        print("\nProcesamiento completado:")
                        print(f"Imagen original: {selected_img['url']}")
                        print(f"Imagen procesada: {result['url']}")
                    else:
                        print("Selección inválida")
            except Exception as e:
                print(f"Error al procesar imagen: {str(e)}")
            
            input("\nPresione Enter para continuar...")
        
        elif choice == '3':
            print_header("PROCESAR IMAGEN LOCAL (CASO 2)")
            try:
                image_path = input("Ingrese la ruta completa a la imagen local: ")
                if os.path.exists(image_path):
                    print(f"\nProcesando {image_path}...")
                    result = client.case2_client_to_server(image_path)
                    print("\nProcesamiento completado:")
                    print(f"Imagen original: {image_path}")
                    print(f"Imagen procesada: {result['url']}")
                else:
                    print(f"Error: No se encontró la imagen en {image_path}")
            except Exception as e:
                print(f"Error al procesar imagen: {str(e)}")
            
            input("\nPresione Enter para continuar...")
        
        elif choice == '4':
            print_header("PROCESAR IMAGEN DEL SERVIDOR Y GUARDAR LOCALMENTE (CASO 3)")
            try:
                images = client.get_server_images()
                if not images:
                    print("No hay imágenes disponibles en el servidor")
                else:
                    print("Imágenes disponibles:")
                    for i, img in enumerate(images):
                        print(f"[{i+1}] {img['name']}")
                    
                    idx = int(input("\nSeleccione el número de imagen a procesar: ")) - 1
                    if 0 <= idx < len(images):
                        selected_img = images[idx]
                        print(f"\nProcesando {selected_img['name']}...")
                        saved_path = client.case3_server_to_client(selected_img['url'], selected_img['name'])
                        print("\nProcesamiento completado:")
                        print(f"Imagen original: {selected_img['url']}")
                        print(f"Imagen guardada en: {saved_path}")
                    else:
                        print("Selección inválida")
            except Exception as e:
                print(f"Error al procesar imagen: {str(e)}")
            
            input("\nPresione Enter para continuar...")
        
        elif choice == '5':
            print_header("CONFIGURACIÓN DEL SERVIDOR")
            new_server = input(f"Ingrese la URL del servidor [{args.server}]: ")
            if new_server.strip():
                args.server = new_server.strip()
                client = ClientServer(args.server)
                print(f"Servidor cambiado a: {args.server}")
            
            input("\nPresione Enter para continuar...")
        
        elif choice == '6':
            print(f"Abriendo interfaz web en: {args.server}")
            webbrowser.open(args.server)
            
            input("\nPresione Enter para continuar...")
        
        else:
            print("Opción inválida. Intente nuevamente.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()