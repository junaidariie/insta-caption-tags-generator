from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List
import requests
from PIL import Image
import io
from utils import (
    load_tagger_model, load_hashtags, find_hashtags,
    load_captioner, generate_captions, load_llm, Generate_post_caption, load_image
)

app = FastAPI(title="Captions and Hashtags Generator", version='1.0')

tagger_model = None
hashtags = None
captions_model = None
llm = None

@app.on_event("startup")
def load_startup_models():
    global tagger_model, hashtags, captions_model, llm
    print("🔁 Loading models (one-time)...")
    tagger_model = load_tagger_model()
    hashtags = load_hashtags()
    captions_model = load_captioner()
    llm = load_llm()
    print("✅ Models loaded once!")


class out_response(BaseModel):
    Mood                :   str
    predicted_caption   :   str
    generated_caption   :   str
    hashtags            :   List[str]

class input_url(BaseModel):
    image_url  :   HttpUrl

@app.get("/")
def Status():
    return {"status" : "The api is live."}

@app.post("/response-upload", response_model=out_response)
async def response(image : UploadFile = File(...)):
    try:
        img_bytes = await image.read()
        processed_image = load_image(img_bytes)
        if processed_image is None:
            raise HTTPException(status_code=400, detail="Could not load the uploaded image")

        generated_image_captions = generate_captions(caption_model=captions_model, image=processed_image)
        if not generated_image_captions:
            raise HTTPException(status_code=500, detail="Caption generation failed")
        
        generated_hashtags = find_hashtags(tagger=tagger_model,image=processed_image, hashtags=hashtags)
        if not generated_hashtags:
            raise HTTPException(status_code=500, detail="Hashtag generation failed")
        
        final_post_captions = Generate_post_caption(top_k_tags=generated_hashtags, predicted_caption=generated_image_captions,llm_model=llm)
        if not final_post_captions:
            raise HTTPException(status_code=500, detail="LLM caption failed")

        return {
            "hashtags"              :   generated_hashtags,
            "predicted_caption"     :   generated_image_captions,
            "Mood"                  :   final_post_captions['Mood'],
            "generated_caption"     :   final_post_captions['Captions']
        }
        

    except:
        raise HTTPException(status_code=400, detail="Error while processing the image")

@app.post("/response-url", response_model=out_response)
def response_url(payload : input_url):
    try:

        url_str = str(payload.image_url)
        processed_image = load_image(url_str)
        if processed_image is None:
            raise HTTPException(status_code=400, detail="Could not load image from given URL")

        generated_image_captions = generate_captions(caption_model=captions_model, image=processed_image)
        if not generated_image_captions:
            raise HTTPException(status_code=500, detail="Caption generation failed")


        generated_hashtags = find_hashtags(tagger=tagger_model,image=processed_image, hashtags=hashtags)
        if not generated_hashtags:
            raise HTTPException(status_code=500, detail="Hashtag generation failed")

        final_post_captions = Generate_post_caption(top_k_tags=generated_hashtags, predicted_caption=generated_image_captions,llm_model=llm)
        if not final_post_captions:
            raise HTTPException(status_code=500, detail="LLM caption failed")

        return {
            "hashtags"              :   generated_hashtags,
            "predicted_caption"     :   generated_image_captions,
            "Mood"                  :   final_post_captions['Mood'],
            "generated_caption"     :   final_post_captions['Captions']
        }
        

    except:
        raise HTTPException(status_code=400, detail="Error while processing the image")