# api/api.py
import io
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn

# Import the logic functions we defined above
# Note: Ensure your project structure allows this import
from mylib.predictor import predict_image, resize_image


app = FastAPI()

# Setup templates directory as requested in Page 1
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Loads the home.html file located in the templates folder.
    """
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint to predict the class of an uploaded image.
    """
    try:
        # Read the file content
        contents = await file.read()

        # Call the logic module
        prediction = predict_image(contents)
        print(f"Prediction: {prediction}")
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "prediction": prediction,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/resize")
async def resize(
    file: UploadFile = File(...), width: int = Form(...), height: int = Form(...)
):
    try:
        contents = await file.read()

        # 1. Llamamos a la lógica, que ahora nos devuelve una imagen PIL
        resized_pil_image = resize_image(contents, width, height)

        # 2. Crear un buffer de bytes en memoria
        buffer = io.BytesIO()

        # 3. Guardar la imagen redimensionada en el buffer
        # Usamos formato PNG para evitar problemas si la imagen original tenía transparencia
        resized_pil_image.save(buffer, format="PNG")

        # 4. Rebobinar el puntero del buffer al principio para leerlo
        buffer.seek(0)

        # 5. Devolver la imagen directamente al navegador
        return StreamingResponse(buffer, media_type="image/png")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# This allows running the API directly if needed, though the PDF suggests specific commands
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
