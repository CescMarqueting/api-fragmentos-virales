from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import yt_dlp
import whisper
import os
from uuid import uuid4
import spacy
import spacy.cli
spacy.cli.download("es_core_news_sm")

app = FastAPI()

# Cargar modelo NLP para análisis avanzado
nlp = spacy.load("es_core_news_sm")

# Modelo para la solicitud
class VideoRequest(BaseModel):
    youtube_url: str

# Función para descargar el video de YouTube
def download_youtube_audio(youtube_url):
    output_path = f"/tmp/{uuid4()}.mp3"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "cookiefile": "/tmp/cookies.txt",  # Usar cookies autenticadas
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    
    # Extraer cookies desde el navegador y guardarlas en /tmp/cookies.txt
    os.system("yt-dlp --cookies-from-browser chrome -o /tmp/cookies.txt")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return output_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error descargando el video: {str(e)}")



# Función para transcribir el audio con Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    return result["segments"]

# Función para analizar el contenido de la transcripción
def analyze_text_for_virality(text):
    doc = nlp(text)
    keywords = ["secreto", "clave", "impactante", "transformación", "descubrí", "revelación", "cambio", "sorprendente"]
    return any(token.text.lower() in keywords for token in doc)

@app.post("/analizar-video")
def analizar_video(request: VideoRequest):
    # Paso 1: Descargar el audio del video
    audio_path = download_youtube_audio(request.youtube_url)

    # Paso 2: Transcribir el audio
    transcription_segments = transcribe_audio(audio_path)

    # Paso 3: Identificar fragmentos virales con análisis avanzado
    candidate_fragments = []
    for segment in transcription_segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]

        # Usar NLP para detectar fragmentos con alto engagement
        if analyze_text_for_virality(text):
            candidate_fragments.append({
                "inicio": f"{int(start_time//60)}:{int(start_time%60):02}",
                "fin": f"{int(end_time//60)}:{int(end_time%60):02}",
                "transcripcion": text,
                "copy_instagram": f"🔥 {text[:100]}... Descúbrelo en la entrevista completa en YouTube!"
            })

        if len(candidate_fragments) >= 2:
            break

    if not candidate_fragments:
        raise HTTPException(status_code=404, detail="No se encontraron fragmentos virales en el video.")

    return {"fragmentos": candidate_fragments}
