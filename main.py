import streamlit as st
from PIL import Image
import time
from utils import (
    load_tagger_model, load_image, load_hashtags, find_hashtags,
    load_captioner, generate_captions, load_llm, Generate_post_caption
)

hf_token = st.secrets["HF_TOKEN"]
openai_key = st.secrets["OPENAI_API_KEY"]



# Page config
st.set_page_config(
    page_title="Instagram Caption Generator",
    page_icon="📸",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.2em;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .process-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 25px;
        border-radius: 12px;
        margin: 15px 0;
        color: white;
        font-size: 1.1em;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    .result-section {
        background: #ffffff;
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
    }
    .mood-display {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.4);
    }
    .mood-emoji {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .mood-text {
        font-size: 1.8em;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .mood-subtitle {
        font-size: 0.9em;
        opacity: 0.9;
        margin-top: 5px;
        font-weight: normal;
        letter-spacing: 1px;
    }
    .caption-display {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
    }
    .caption-text {
        font-size: 1.5em;
        font-style: italic;
        line-height: 1.6;
        text-align: center;
        font-weight: 500;
    }
    .hashtag-display {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 6px 20px rgba(67, 233, 123, 0.4);
    }
    .hashtag-text {
        font-size: 1.2em;
        font-weight: 600;
        text-align: center;
        word-wrap: break-word;
        line-height: 1.8;
    }
    .section-title {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .copy-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        margin-top: 10px;
    }
    .dots-loader {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        padding: 20px;
    }
    .dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        animation: bounce 1.4s infinite ease-in-out both;
    }
    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }
    .dot:nth-child(3) { animation-delay: 0s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
    }
    .generate-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-size: 1.3em !important;
        font-weight: bold !important;
        padding: 15px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    .generate-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6) !important;
    }
    .footer-tech {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        flex-wrap: wrap;
        margin-bottom: 15px;
    }
    .tech-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .footer-creator {
        text-align: center;
        font-size: 1.1em;
        color: #666;
        font-weight: 500;
        margin-top: 10px;
    }
    .image-description {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin-top: 15px;
    }
    .step-icon {
        font-size: 1.5em;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📸 Instagram Caption Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">✨ Transform your images into engaging Instagram posts with AI magic!</div>', unsafe_allow_html=True)

# Initialize session state for models
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = False
    st.session_state.tagger_model = None
    st.session_state.hashtags = None
    st.session_state.captions_model = None
    st.session_state.llm = None

# Load models with progress
if not st.session_state.models_loaded:
    loader_placeholder = st.empty()
    loader_placeholder.markdown('<div class="dots-loader"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("⚙️ Loading hashtag recognition model...")
    st.session_state.tagger_model = load_tagger_model()
    progress_bar.progress(25)
    time.sleep(0.3)
    
    status_text.text("📚 Loading hashtag database...")
    st.session_state.hashtags = load_hashtags()
    progress_bar.progress(50)
    time.sleep(0.3)
    
    status_text.text("🎨 Loading caption generation model...")
    st.session_state.captions_model = load_captioner()
    progress_bar.progress(75)
    time.sleep(0.3)
    
    status_text.text("🤖 Loading AI language model...")
    st.session_state.llm = load_llm()
    progress_bar.progress(100)
    time.sleep(0.3)
    
    st.session_state.models_loaded = True
    
    # Clear all loading indicators
    loader_placeholder.empty()
    progress_bar.empty()
    status_text.empty()
    
    success_msg = st.success('✅ All AI models loaded and ready!')
    time.sleep(1)
    success_msg.empty()

# Image input section
st.markdown("---")
st.subheader("📤 Upload Your Image")

input_method = st.radio(
    "Choose input method:",
    ["📁 Upload Image File", "🔗 Image URL"],
    horizontal=True
)

image = None
image_path = None

if input_method == "📁 Upload Image File":
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif', 'tiff', 'tif', 'ico', 'jfif', 'pjpeg', 'pjp'],
        help="Supports: PNG, JPG, JPEG, WEBP, BMP, GIF, TIFF, ICO and more!"
    )
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_path = uploaded_file
else:
    image_url = st.text_input(
        "Enter image URL:",
        placeholder="https://example.com/image.jpg"
    )
    if image_url:
        loader_placeholder = st.empty()
        loader_placeholder.markdown('<div class="dots-loader"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
        image = load_image(image_url)
        if image:
            image_path = image_url
            loader_placeholder.empty()
            st.success("✓ Image loaded successfully!")

# Display image and generate button
if image:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Your Selected Image", use_container_width=True)
    
    st.markdown("---")
    
    # Generate button with custom styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_clicked = st.button("✨ Generate Magic ✨", key="generate_btn", use_container_width=True)
    
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 1.3em;
            font-weight: bold;
            padding: 15px 40px;
            border-radius: 50px;
            border: none;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
        }
        </style>
    """, unsafe_allow_html=True)
    
    if generate_clicked:
        
        # Create a container for the generation process
        process_container = st.container()
        
        with process_container:
            st.markdown("### 🔄 AI Processing Pipeline")
            
            # Step 1: Generate image caption
            step1_placeholder = st.empty()
            step1_placeholder.markdown(
                '<div class="process-step"><span class="step-icon">🎨</span>Step 1: Analyzing image content and generating description...</div>',
                unsafe_allow_html=True
            )
            
            loader1 = st.empty()
            loader1.markdown('<div class="dots-loader"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
            time.sleep(0.8)
            generated_image_captions = generate_captions(
                caption_model=st.session_state.captions_model,
                image=image
            )
            
            if generated_image_captions:
                loader1.empty()
                step1_placeholder.markdown(
                    f'<div class="process-step"><span class="step-icon">✅</span>Step 1 Complete: Found "{generated_image_captions}"</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.5)
            
            # Step 2: Generate hashtags
            step2_placeholder = st.empty()
            step2_placeholder.markdown(
                '<div class="process-step"><span class="step-icon">🔍</span>Step 2: Searching through database for perfect hashtags...</div>',
                unsafe_allow_html=True
            )
            
            loader2 = st.empty()
            loader2.markdown('<div class="dots-loader"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
            time.sleep(0.8)
            generated_hashtags = find_hashtags(
                tagger=st.session_state.tagger_model,
                image=image,
                hashtags=st.session_state.hashtags
            )
            
            if generated_hashtags:
                loader2.empty()
                # Get 8 hashtags instead of 5
                generated_hashtags = generated_hashtags[:8] if len(generated_hashtags) > 8 else generated_hashtags
                hashtags_preview = " ".join(generated_hashtags[:3]) + "..."
                step2_placeholder.markdown(
                    f'<div class="process-step"><span class="step-icon">✅</span>Step 2 Complete: Found {len(generated_hashtags)} hashtags ({hashtags_preview})</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.5)
            
            # Step 3: Generate final caption with LLM
            step3_placeholder = st.empty()
            step3_placeholder.markdown(
                '<div class="process-step"><span class="step-icon">✍️</span>Step 3: AI is crafting your perfect Instagram caption...</div>',
                unsafe_allow_html=True
            )
            
            loader3 = st.empty()
            loader3.markdown('<div class="dots-loader"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
            time.sleep(0.8)
            final_post_captions = Generate_post_caption(
                top_k_tags=generated_hashtags,
                predicted_caption=generated_image_captions,
                llm_model=st.session_state.llm
            )
            
            if final_post_captions:
                loader3.empty()
                step3_placeholder.markdown(
                    '<div class="process-step"><span class="step-icon">✅</span>Step 3 Complete: Caption ready to post!</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.5)
        
        # Display results with beautiful formatting
        st.markdown("---")
        st.markdown("## 🎉 Your Instagram Post is Ready!")
        
        results_container = st.container()
        
        with results_container:
            # Mood Section with better explanation
            if final_post_captions and 'Mood' in final_post_captions:
                time.sleep(0.4)
                mood_emojis = {
                    'happy': '😊', 'joyful': '😄', 'excited': '🤩', 'peaceful': '😌',
                    'calm': '😊', 'energetic': '⚡', 'playful': '😜', 'serene': '🧘',
                    'fun': '🎉', 'cheerful': '😁', 'relaxed': '😎', 'vibrant': '🌟',
                    'cozy': '🥰', 'adventurous': '🗺️', 'dreamy': '💭', 'romantic': '💕'
                }
                
                mood_lower = final_post_captions["Mood"].lower()
                emoji = '✨'
                for key, value in mood_emojis.items():
                    if key in mood_lower:
                        emoji = value
                        break
                
                st.markdown(f"""
                    <div class="mood-display">
                        <div class="mood-emoji">{emoji}</div>
                        <div class="mood-text">{final_post_captions["Mood"]}</div>
                        <div class="mood-subtitle">Vibe of your image</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Caption Section
            if final_post_captions and 'Captions' in final_post_captions:
                time.sleep(0.4)
                st.markdown(f"""
                    <div class="caption-display">
                        <div class="section-title">💬 Your Caption</div>
                        <div class="caption-text">"{final_post_captions["Captions"]}"</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Copy button for caption
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.code(final_post_captions["Captions"], language=None)
            
            # Hashtags Section
            if generated_hashtags:
                time.sleep(0.4)
                hashtags_formatted = " ".join(generated_hashtags)
                st.markdown(f"""
                    <div class="hashtag-display">
                        <div class="section-title">🏷️ Hashtags ({len(generated_hashtags)} tags)</div>
                        <div class="hashtag-text">{hashtags_formatted}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Copy button for hashtags
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.code(hashtags_formatted, language=None)
            
            # AI Image Description (expandable)
            with st.expander("🔍 View Technical Details - AI Image Analysis"):
                if generated_image_captions:
                    st.markdown(f"""
                        <div class="image-description">
                            <strong>AI Vision Model Description:</strong><br>
                            {generated_image_captions}
                        </div>
                    """, unsafe_allow_html=True)
            
            # Success animation
            st.balloons()
            time.sleep(0.5)
            st.success("🎊 Perfect! Your Instagram post is ready. Copy and paste to your post!")
            
            # Pro tip
            st.info("💡 **Pro Tip:** Copy the caption and hashtags separately for better Instagram formatting!")

else:
    # Empty state with nice styling
    st.markdown("""
        <div style='text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-radius: 15px; margin: 20px 0;'>
            <h2 style='color: #667eea;'>👆 Get Started</h2>
            <p style='font-size: 1.2em; color: #666;'>Upload an image or provide a URL to generate your Instagram caption!</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='padding: 30px 20px;'>
        <div class="footer-tech">
            <span class="tech-badge">🤖 GPT-4</span>
            <span class="tech-badge">🎯 CLIP</span>
            <span class="tech-badge">🎨 GIT-Base</span>
        </div>
        <div class="footer-creator">
            Crafted with 💜 for Content Creators Worldwide 🌍
        </div>
    </div>

""", unsafe_allow_html=True)
