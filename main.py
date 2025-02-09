from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import whisper
import torch

# Verificar si hay GPU disponible
device = "cuda" if torch.cuda.is_available() else "cpu"

# Cargar el modelo de Whisper
try:
    model = whisper.load_model("small", device=device)
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo de Whisper: {str(e)}")


# Endpoint para transcribir el video
@app.post("/transcribir/")
async def transcribir_video(file: UploadFile = File(...)):
    try:
        # Guardar el archivo en el servidor
        file_location = f"{UPLOAD_DIR}/{uuid4()}-{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Cargar el modelo de Whisper
        import whisper

try:
    model = whisper.load_model("small")
except AttributeError:
    import torch
    model = whisper.Whisper.load_model("small", device="cpu" if not torch.cuda.is_available() else "cuda")

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
