from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
import os

app = FastAPI()

# Mount static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def change_image(request: Request, file: UploadFile = File(...)):
    # Load the image
    image = Image.open(io.BytesIO(await file.read()))

    # Save the original image
    original_image_path = "static/original_image.png"
    image.save(original_image_path)

    # Convert image to grayscale
    image_gray = image.convert("L")

    # Resize the grayscale image to a specific size
    specific_size = (300, 300)
    image_resized = image_gray.resize(specific_size)

    # Save the resized grayscale image to a file
    processed_image_path = "static/processed_image.png"
    image_gray.save(processed_image_path)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "original_image_path": original_image_path,
        "processed_image_path": processed_image_path
    })

@app.get("/static/{image_name}", response_class=FileResponse)
async def get_image(image_name: str):
    return FileResponse(f"static/{image_name}")
