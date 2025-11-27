import click
from mylib.predictor import *
@click.group()
def ml():
    """Herramientas de Machine Learning para procesamiento de imágenes."""
    pass

@ml.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--width', '-w', required=True, type=int, help='Nuevo ancho de la imagen.')
@click.option('--height', '-h', required=True, type=int, help='Nuevo alto de la imagen.')
@click.option('--output', '-o', default='resized_output.png', help='Ruta del archivo de salida.')
def resize(input_path, width, height, output):
    """Redimensiona una imagen dada."""
    
    # Leemos el archivo local como bytes
    with open(input_path, "rb") as f:
        image_bytes = f.read()
    
    try:
        # Llamamos a tu lógica
        result_img = resize_image(image_bytes, width, height)
        
        # Guardamos el resultado (necesario en CLI)
        result_img.save(output)
        click.secho(f"✅ Imagen redimensionada guardada en: {output}", fg="green")
        click.echo(f"Nuevas dimensiones: {result_img.size}")
        
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")

@ml.command()
@click.argument('input_path', type=click.Path(exists=True))
def predict(input_path):
    """Predice si una imagen es clara u oscura."""
    
    # Leemos el archivo local como bytes
    with open(input_path, "rb") as f:
        image_bytes = f.read()
        
    # Llamamos a tu lógica
    result = predict_image(image_bytes)
    
    # Imprimimos el resultado
    if "Error" in result:
        click.secho(result, fg="red")
    else:
        color = "yellow" if result == "Bright Image" else "blue"
        click.secho(f"Predicción: {result}", fg=color, bold=True)

if __name__ == '__main__':
    ml()