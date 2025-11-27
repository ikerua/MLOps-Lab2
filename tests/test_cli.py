import os
from click.testing import CliRunner
from PIL import Image
# Ajusta la importación al nombre de tu archivo cli, ej: from cli.cli import ml
from cli.cli import ml 

def create_dummy_image(filename):
    """Ayuda para crear una imagen física en el sistema de archivos aislado."""
    img = Image.new('RGB', (100, 100), color='white')
    img.save(filename)

def test_cli_predict():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # 1. Crear imagen dummy
        create_dummy_image("test_img.jpg")
        
        # 2. Ejecutar comando
        result = runner.invoke(ml, ['predict', 'test_img.jpg'])
        
        # 3. Validaciones
        assert result.exit_code == 0
        assert "Bright Image" in result.output

def test_cli_resize():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # 1. Crear imagen dummy
        create_dummy_image("input.jpg")
        
        # 2. Ejecutar comando resize
        result = runner.invoke(ml, [
            'resize', 'input.jpg', 
            '--width', '50', 
            '--height', '50', 
            '-o', 'output.png'
        ])
        
        # 3. Validar ejecución
        assert result.exit_code == 0
        assert "Imagen redimensionada guardada" in result.output
        
        # 4. Validar que el archivo de salida existe y es correcto
        assert os.path.exists("output.png")
        img = Image.open("output.png")
        assert img.size == (50, 50)

def test_cli_file_not_found():
    """Prueba que Click valide la existencia del archivo (Path(exists=True))."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(ml, ['predict', 'non_existent.jpg'])
        
        # Debe fallar porque el archivo no existe
        assert result.exit_code != 0
        assert "Invalid value for 'INPUT_PATH'" in result.output or "does not exist" in result.output