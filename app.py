import streamlit as st
import base64
import openai
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
openai.api_key = os.getenv("API_AI_KEY")

# Page config
st.set_page_config(
    page_title="Text to Image Generator",
    page_icon="🎨",
    layout="centered"
)

def call_api(prompt):
    """Generate image using OpenAI API"""
    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    return base64.b64decode(response.data[0].b64_json)

def main():
    st.title("🎨 Text to Image Generator")
    st.write("Enter a prompt to generate an image using AI")
    
    # Input section
    prompt = st.text_input(
        "Enter your prompt:",
        placeholder="e.g., A beautiful sunset over mountains"
    )
    
    # Generate button
    if st.button("Generate Image", type="primary"):
        if prompt:
            with st.spinner("Generating image..."):
                try:
                    # Generate image
                    image_bytes = call_api(prompt)
                    
                    # Convert to PIL Image for display
                    image = Image.open(BytesIO(image_bytes))
                    
                    # Store in session state
                    st.session_state.generated_image = image_bytes
                    st.session_state.generated_pil_image = image
                    st.session_state.prompt_used = prompt
                    
                    st.success("Image generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating image: {str(e)}")
        else:
            st.warning("Please enter a prompt first!")
    
    # Display generated image if it exists
    if hasattr(st.session_state, 'generated_pil_image'):
        st.divider()
        st.subheader("Generated Image")
        st.write(f"**Prompt:** {st.session_state.prompt_used}")
        
        # Display image
        st.image(st.session_state.generated_pil_image)
        
        # Download button
        st.download_button(
            label="💾 Download Image",
            data=st.session_state.generated_image,
            file_name="generated_image.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()