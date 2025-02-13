from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load API keys from .env file

app = FastAPI()

# Predefined sizes
SIZES = [(300, 250), (728, 90), (160, 600), (300, 600)]

# Twitter API credentials (store in .env file)
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"
TWEET_URL = "https://api.twitter.com/2/tweets"

def resize_image(image: Image.Image, size: tuple):
    return image.resize(size, Image.ANTIALIAS)

@app.post("/api/process-image")
async def process_image(image: UploadFile = File(...)):
    try:
        # Read image
        image_data = await image.read()
        img = Image.open(io.BytesIO(image_data))

        resized_images = []
        for size in SIZES:
            resized_img = resize_image(img, size)
            img_io = io.BytesIO()
            resized_img.save(img_io, format="JPEG")
            img_io.seek(0)
            resized_images.append(img_io)

        # (Twitter API upload logic goes here)

        return JSONResponse(content={"message": "Images resized and posted!"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
