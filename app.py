import gradio as gr
import requests
from PIL import Image
import io
# URL of the API created with FastAPI
API_URL = "https://predictor-api-4pbm.onrender.com"



def solicitar_prediccion(image_path):
    """
    Envía la imagen al endpoint /predict
    """
    if image_path is None:
        return "Por favor, sube una imagen primero."
    
    try:
        # Abrimos la imagen en modo binario para enviarla
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{API_URL}/predict", files=files, timeout=10)
            
        response.raise_for_status()
        data = response.json()
        
        # Devolvemos la predicción
        return f"Predicción: {data.get('prediction')}"
        
    except requests.exceptions.RequestException as e:
        return f"Error en la conexión con la API: {str(e)}"
    except Exception as e:
        return f"Error desconocido: {str(e)}"

def solicitar_resize(image_path, width, height):
    """
    Envía la imagen y dimensiones al endpoint /resize
    """
    if image_path is None:
        return None
    
    try:
        # Validar inputs
        if width <= 0 or height <= 0:
            print("El ancho y alto deben ser positivos.")
            return None

        payload = {"width": int(width), "height": int(height)}
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            # Nota: 'data' se usa para los campos del Form (width, height)
            # y 'files' para el archivo
            response = requests.post(f"{API_URL}/resize", data=payload, files=files, timeout=10)
            
        response.raise_for_status()
        
        # La API devuelve una imagen en bytes (StreamingResponse)
        # La convertimos a objeto PIL Image para que Gradio la pueda mostrar
        image_stream = io.BytesIO(response.content)
        return Image.open(image_stream)
        
    except requests.exceptions.RequestException as e:
        print(f"Error API: {e}")
        return None

# --- Construcción de la Interfaz con Blocks ---
with gr.Blocks(title="Predictor & Resizer API Client") as demo:
    gr.Markdown("# Cliente para API de Imágenes")
    gr.Markdown("Sube una imagen y elige si quieres obtener una predicción o redimensionarla.")

    with gr.Row():
        # Columna Izquierda: Entrada
        with gr.Column():
            gr.Markdown("### 1. Entrada")
            # Selector de imágenes. 'type="filepath"' guarda la imagen temporalmente y nos da la ruta
            input_image = gr.Image(label="Sube tu imagen", type="filepath")

        # Columna Derecha: Acciones
        with gr.Column():
            
            # --- Sección de Predicción ---
            gr.Markdown("### 2. Predicción")
            predict_btn = gr.Button("🔍 Obtener Predicción", variant="primary")
            predict_output = gr.Textbox(label="Resultado de la API")

            gr.Html("<hr>") # Separador visual

            # --- Sección de Resize ---
            gr.Markdown("### 3. Redimensionar (Resize)")
            with gr.Row():
                w_input = gr.Number(label="Ancho (Width)", value=200, precision=0)
                h_input = gr.Number(label="Alto (Height)", value=200, precision=0)
            
            resize_btn = gr.Button("🖼️ Redimensionar Imagen")
            resize_output = gr.Image(label="Imagen Redimensionada")

    # --- Conectar la lógica ---
    
    # Botón Predicción
    predict_btn.click(
        fn=solicitar_prediccion,
        inputs=[input_image],
        outputs=predict_output
    )

    # Botón Resize
    resize_btn.click(
        fn=solicitar_resize,
        inputs=[input_image, w_input, h_input],
        outputs=resize_output
    )
# Lanzar la aplicación
if __name__ == "__main__":
    demo.launch()