from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import whisper
import os
from uuid import uuid4
import shutil

app = FastAPI()

# Carpeta temporal para archivos subidos
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Modelo de solicitud para la transcripción manual
class TranscriptionRequest(BaseModel):
    transcription: str

# Endpoint para subir el archivo de video
@app.post("/subir-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Guardar el archivo en el servidor
        file_location = f"{UPLOAD_DIR}/{uuid4()}-{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"mensaje": "Archivo subido correctamente", "ruta": file_location}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")

# Endpoint para transcribir el video
@app.post("/transcribir/")
async def transcribir_video(file: UploadFile = File(...)):
    try:
        # Guardar el archivo en el servidor
        file_location = f"{UPLOAD_DIR}/{uuid4()}-{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Cargar el modelo de Whisper
        model = whisper.load_model("small")
        result = model.transcribe(file_location)

        return {"transcripcion": result["text"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al transcribir el video: {str(e)}")

# Endpoint para subir un archivo de subtítulos opcional (.vtt)
@app.post("/subir-subtitulos/")
async def upload_subtitles(file: UploadFile = File(...)):
    try:
        file_location = f"{UPLOAD_DIR}/{uuid4()}-{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"mensaje": "Archivo de subtítulos subido correctamente", "ruta": file_location}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo de subtítulos: {str(e)}")
