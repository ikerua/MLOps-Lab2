import io
import pytest
import numpy as np
from PIL import Image
from mylib.predictor import resize_image, predict_image

@pytest.fixture
def dark_image_bytes():
    """Crea una imagen negra (oscura) en memoria."""
    img = Image.new('RGB', (100, 100), color='black')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

@pytest.fixture
def bright_image_bytes():
    """Crea una imagen blanca (clara) en memoria."""
    img = Image.new('RGB', (100, 100), color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def test_resize_image_success(dark_image_bytes):
    """Prueba que la imagen se redimensiona correctamente."""
    target_w, target_h = 50, 50
    resized_img = resize_image(dark_image_bytes, target_w, target_h)
    
    assert isinstance(resized_img, Image.Image)
    assert resized_img.size == (target_w, target_h)

def test_resize_image_invalid_data():
    """Prueba que lance error con datos corruptos."""
    with pytest.raises(ValueError):
        resize_image(b"not an image", 100, 100)

def test_predict_dark_image(dark_image_bytes):
    """Prueba la predicción de imagen oscura."""
    result = predict_image(dark_image_bytes)
    assert result == "Dark Image"

def test_predict_bright_image(bright_image_bytes):
    """Prueba la predicción de imagen clara."""
    result = predict_image(bright_image_bytes)
    assert result == "Bright Image"

def test_predict_error_handling():
    """Prueba que el manejador de errores de predict devuelva el string de error."""
    result = predict_image(b"basura")
    assert "Error processing image" in result