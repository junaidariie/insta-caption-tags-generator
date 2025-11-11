# 📸 Insta Caption & Hashtag Generator

A smart AI-powered Streamlit application that automatically generates **Instagram-style captions**, **moods**, and **top hashtags** from any uploaded image.  
Just upload an image → the app analyzes it → instantly gives creative captions and relevant tags.

🚀 **Live App:**  
👉 https://insta-captions-and-hashtags-generator-qgsgpoyydvy4fwkeakzncz.streamlit.app/

---

## ✅ Features

- ✅ **AI Image Captioning** – Generates a meaningful caption from the image  
- ✅ **Mood Detection** – Determines the image’s emotional tone in 1–2 words  
- ✅ **Hashtag Prediction** – Picks the best matching hashtags using zero-shot classification  
- ✅ **Clean UI Built with Streamlit** – Fast, simple, and responsive  
- ✅ **Support for URL and File Upload**  
- ✅ **Optimized for CPU environments** – Works even without GPU

---

## 🧠 Tech Behind the App

| Component | Library / Model |
|-----------|-----------------|
| Caption Generation | `microsoft/git-base` (image-to-text) |
| Hashtag Prediction | `openai/clip-vit-base-patch32` (zero-shot classification) |
| LLM Caption Polishing | OpenAI GPT-4.1-nano (via LangChain) |
| Frontend | Streamlit |
| Backend API | FastAPI (complete backend already built) |

✅ The code is modular:  
- `load_image()` handles URLs, uploaded files, or local paths  
- Separate utilities for tagging, captioning, and LLM enhancement  
- Pydantic parsing ensures structured LLM responses

---

## 🖥️ Live Demo

Click below, upload an image, and get captions & tags instantly:

👉 **https://insta-captions-and-hashtags-generator-qgsgpoyydvy4fwkeakzncz.streamlit.app/**

---

## 🧩 Project Architecture

```
User uploads image ─▶ Caption Model (GIT)
                    ─▶ Mood + Poetic Caption (GPT via LangChain)
                    ─▶ CLIP Model predicts best hashtags
                    ─▶ Final Output (Mood + Caption + Top Tags)
```

✅ Hashtags are loaded from a curated dataset  
✅ CLIP scores each label and picks the best matches  
✅ Output is clean, short, Instagram-friendly

---

## 🧪 Local Installation

### 1. Clone repository
```bash
git clone https://github.com/junaidariie/insta-caption-tags-generator.git
cd insta-caption-tags-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API keys  
Create a `.streamlit/secrets.toml`:

```toml
HF_TOKEN="your_huggingface_token"
OPENAI_API_KEY="your_openai_key"
```

### 4. Run Streamlit app
```bash
streamlit run app.py
```

---

## 🔗 FastAPI Backend (API Support)

A full **FastAPI backend** is already implemented, so this project can be deployed as a real production API.

- Clean endpoint structure  
- Pydantic validation  
- Can be plugged into mobile apps / web apps  
- If cloud service access was available (AWS, Azure, Render), the API could be deployed live as well

✅ Right now, only Streamlit Cloud is used because other cloud platforms require card verification.

---

## 📁 Folder Structure

```
insta-caption-tags-generator/
│── app.py                 # Streamlit UI
│── tag_utils.py           # Hashtag model + scoring
│── caption_utils.py       # Caption model logic
│── llm_utils.py           # GPT-based caption polishing
│── instagram_hashtags_210.txt
│── requirements.txt
```

---

## ✅ Future Enhancements

✅ Add auto-generated hashtags for multiple languages  
✅ Deploy FastAPI backend when a cloud provider is available  
✅ Create bulk captioning for photographers/social media managers  
✅ Add downloading: caption + tags in one click  
✅ Save image history for logged-in users

---

## 📸 Screenshots
(Add screenshots here once available)
- Upload Page
- Generated Output (Mood, Caption, Tags)

---

### 💡 About the Project
Built by **Junaid**, focusing on practical AI/ML applications using vision models, LLMs, and real deployment. This app demonstrates:
- Zero-shot image classification
- Image captioning
- Combining HuggingFace + LangChain + Streamlit
- API-ready code architecture

---

### ⭐ Want to Contribute?
Feel free to fork, open issues, or improve models/UX.

---

### ✅ If you like the project, give the repo a ⭐ on GitHub!
