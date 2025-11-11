from transformers import pipeline
import requests
from langchain_openai import ChatOpenAI
from PIL import Image
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import io
import streamlit as st
load_dotenv()


hf_token = st.secrets["HF_TOKEN"]
openai_key = st.secrets["OPENAI_API_KEY"]



#------------------TAGGER UTILITIES--------------------
#-----------------------load model------------------------
def load_tagger_model():
    try:
        tagger = pipeline(
        "zero-shot-image-classification",
        model="openai/clip-vit-base-patch32",
        token=hf_token)
        return tagger
    except Exception as e:
        print("Error loading model:", e)
        return None

#---------------------load image---------------------------
def load_image(image_path) -> Image.Image:
    try:
        if isinstance(image_path, bytes):
            img = Image.open(io.BytesIO(image_path)).convert("RGB")
            return img
        if isinstance(image_path, str) and image_path.startswith(("http://", "https://")):
            img = Image.open(requests.get(image_path, stream=True, timeout=20).raw).convert("RGB")
            return img
        if isinstance(image_path, str):
            img = Image.open(image_path).convert("RGB")
            return img
        return None
    except Exception as e:
        print(f"Found an unexpected error while loading the image : {e}")
        return None

#-------------------loading hastags---------------------------
def load_hashtags():
    try:
        with open("instagram_hashtags_210.txt", "r", encoding="utf-8") as f:
            hashtags = f.read().splitlines()
        st.write(f"Loaded {len(hashtags)} hashtags") 
        return hashtags
    except Exception as e:
        st.error(f"Error while loading hashtags: {e}")
        return None
    
def find_hashtags(tagger, image, hashtags): 
    try:
        top_k_tags = []
        results = tagger(image, hashtags)
        sorted_tags = sorted(results, key=lambda x:x["score"], reverse=True)
        for tags in sorted_tags[:5]:
            top_k_tags.append(tags["label"])
        return top_k_tags
    except Exception as e:
        print("Could not find the hashtags due to unxepected error : ",e)
        return None
    

#------------------CAPTIONER UTILITIES--------------------
#------------------Captions Model-------------------------
def load_captioner():
    try:
        captions = pipeline(
        task="image-to-text",
        model="microsoft/git-base")
        return captions
    except Exception as e:
        print("Got an error while loading the model : ", e)
        return None
    
#-------------------Generate captions---------------------
def generate_captions(caption_model, image):
    try:
        captions = caption_model(image)
        return captions[0]['generated_text']
    except Exception as e:
        print("Error while generating caption for image : ", e)
        return None

#------------------LLM UTILITIES--------------------
#-------------------Load LLM------------------------
def load_llm():
    try:
        llm = ChatOpenAI(model="gpt-4.1-nano", streaming=True)
        return llm
    except Exception as e:
        print("Erro while loading llm : ", e)
        return None
    
#-------------------Post Caption Generator-----------
class CaptionOutput(BaseModel):
    Mood: str
    Caption: str

out_parse = PydanticOutputParser(pydantic_object=CaptionOutput)

def Generate_post_caption(top_k_tags, predicted_caption, llm_model):
    try:
        prompt = PromptTemplate(
        input_variables=["caption", "tags"],
        partial_variables={"format_instructions": out_parse.get_format_instructions()},
        template="""
        Given this image caption: "{caption}"
        and tags: {tags},
        describe the overall MOOD of the image in 1-2 words, and
        write a short, poetic Instagram-style caption (max 10 words).

        Output format:
        Mood: <mood>
        Caption: <caption>
        {format_instructions}
        """
        )
        chain = prompt | llm_model | out_parse
        results = chain.invoke({
        "caption": predicted_caption,
        "tags": top_k_tags
        })  
        return {
            "Mood" : results.Mood,
            "Captions" : results.Caption
        }
    except Exception as e:
        print("Error while generating Caption for Image : ", e)

        return None




