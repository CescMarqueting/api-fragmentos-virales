{\rtf1\ansi\ansicpg1252\cocoartf2708
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Bold;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\b\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 from fastapi import FastAPI, HTTPException\
from pydantic import BaseModel\
import subprocess\
import yt_dlp\
import whisper\
import os\
from uuid import uuid4\
import spacy\
\
app = FastAPI()\
\
# Cargar modelo NLP para an\'e1lisis avanzado\
nlp = spacy.load("es_core_news_sm")\
\
# Modelo para la solicitud\
class VideoRequest(BaseModel):\
    youtube_url: str\
\
# Funci\'f3n para descargar el video de YouTube\
def download_youtube_audio(youtube_url):\
    output_path = f"/tmp/\{uuid4()\}.mp3"\
    ydl_opts = \{\
        'format': 'bestaudio/best',\
        'outtmpl': output_path,\
        'postprocessors': [\{\
            'key': 'FFmpegExtractAudio',\
            'preferredcodec': 'mp3',\
            'preferredquality': '192',\
        \}],\
    \}\
    try:\
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:\
            ydl.download([youtube_url])\
        return output_path\
    except Exception as e:\
        raise HTTPException(status_code=500, detail=f"Error descargando el video: \{str(e)\}")\
\
# Funci\'f3n para transcribir el audio con Whisper\
def transcribe_audio(audio_path):\
    model = whisper.load_model("small")\
    result = model.transcribe(audio_path)\
    return result["segments"]\
\
# Funci\'f3n para analizar el contenido de la transcripci\'f3n\
def analyze_text_for_virality(text):\
    doc = nlp(text)\
    keywords = ["secreto", "clave", "impactante", "transformaci\'f3n", "descubr\'ed", "revelaci\'f3n", "cambio", "sorprendente"]\
    return any(token.text.lower() in keywords for token in doc)\
\
@app.post("/analizar-video")\
def analizar_video(request: VideoRequest):\
    # Paso 1: Descargar el audio del video\
    audio_path = download_youtube_audio(request.youtube_url)\
\
    # Paso 2: Transcribir el audio\
    transcription_segments = transcribe_audio(audio_path)\
\
    # Paso 3: Identificar fragmentos virales con an\'e1lisis avanzado\
    candidate_fragments = []\
    for segment in transcription_segments:\
        start_time = segment["start"]\
        end_time = segment["end"]\
        text = segment["text"]\
\
        # Usar NLP para detectar fragmentos con alto engagement\
        if analyze_text_for_virality(text):\
            candidate_fragments.append(\{\
                "inicio": f"\{int(start_time//60)\}:\{int(start_time%60):02\}",\
                "fin": f"\{int(end_time//60)\}:\{int(end_time%60):02\}",\
                "transcripcion": text,\
                "copy_instagram": f"\uc0\u55357 \u56613  \{text[:100]\}... Desc\'fabrelo en la entrevista completa en YouTube!"\
            \})\
\
        if len(candidate_fragments) >= 2:\
            break\
\
    if not candidate_fragments:\
        raise HTTPException(status_code=404, detail="No se encontraron fragmentos virales en el video.")\
\
    return \{"fragmentos": candidate_fragments\}\
}
# Pequeño cambio para forzar redeploy en Render
