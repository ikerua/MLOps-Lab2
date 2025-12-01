import io
from PIL import Image
import numpy as np


def resize_image(image_bytes, width, height):
    """
    Recibe bytes de imagen, la redimensiona y devuelve las nuevas dimensiones.
    """
    try:
        # 1. Convertir bytes a objeto Imagen
        image = Image.open(io.BytesIO(image_bytes))

        # 2. Redimensionar
        resized_img = image.resize((width, height))

        # Devolvemos el tamaño para que la API pueda imprimirlo en el mensaje
        return resized_img
    except Exception as e:
        raise ValueError(f"No se pudo procesar la imagen para redimensionar: {e}") from e


def predict_image(image_bytes):
    """
    Recibe bytes de imagen, la decodifica a píxeles y calcula el brillo.
    """
    try:
        # 1. Convertir bytes a objeto Imagen
        image = Image.open(io.BytesIO(image_bytes))

        # 2. Convertir a RGB para asegurar 3 canales (evita errores con PNG transparentes)
        image = image.convert("RGB")

        # 3. Ahora sí, convertir a array de Numpy (ahora son números, no bytes crudos)
        image_array = np.array(image)

        # 4. Lógica de predicción
        mean_pixel_value = np.mean(image_array)

        if mean_pixel_value > 127:
            return "Bright Image"
        else:
            return "Dark Image"

    except (IOError, ValueError) as e:
        # Esto atrapará si el archivo subido no es una imagen válida
        return f"Error processing image: {str(e)}"
