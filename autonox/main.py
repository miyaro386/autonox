import io
from glob import glob
from random import choice

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
from PIL import Image
from numpy.ma.core import array

app = FastAPI()

origins = ["http://localhost:3001", ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"Hello": "World!!!!!!!!!!!!!!!!!!"}


@app.get("/img")
def img():
    paths = glob("dataset/**/*.png", recursive=True)
    path = choice(paths)
    img = cv2.imread(path)
    img = Image.fromarray(img)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return StreamingResponse(img_bytes, media_type="image/png")
