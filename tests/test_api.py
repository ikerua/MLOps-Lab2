import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
# Ajusta la importación según tu estructura real, ej: from api.api import app
from api.api import app 

client = TestClient(app)

@pytest.fixture
def image_file():
    """Genera bytes de una imagen válida para subir."""
    img = Image.new('RGB', (100, 100), color='red')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def test_api_predict_endpoint(image_file):
    """Prueba el endpoint POST /predict."""
    files = {'file': ('test.png', image_file, 'image/png')}
    response = client.post("/predict", files=files)
    
    assert response.status_code == 200
    json_resp = response.json()
    assert "prediction" in json_resp
    # Como la imagen es roja pura (intensidad media), verificamos que devuelva una predicción válida
    assert json_resp["prediction"] in ["Bright Image", "Dark Image"]

def test_api_resize_endpoint(image_file):
    """Prueba el endpoint POST /resize."""
    files = {'file': ('test.png', image_file, 'image/png')}
    data = {'width': 50, 'height': 50}
    
    response = client.post("/resize", files=files, data=data)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Verificar que la imagen devuelta tiene el tamaño correcto
    returned_img = Image.open(io.BytesIO(response.content))
    assert returned_img.size == (50, 50)

def test_api_predict_bad_file():
    """Prueba enviar un archivo corrupto al endpoint predict."""
    files = {'file': ('bad.txt', b'not an image', 'text/plain')}
    response = client.post("/predict", files=files)
    
    # Dependiendo de cómo predictor maneje el error, api devuelve 200 con mensaje o 400.
    # En tu código api.py atrapas ValueError y lanzas 400, pero predict_image retorna string "Error..."
    # Si predict_image no lanza excepción, la API devolverá 200 con el string de error en el JSON.
    assert response.status_code == 200 
    assert "Error processing image" in response.json()["prediction"]