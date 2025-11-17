import streamlit as st
from PIL import Image
from io import BytesIO
import os
import traceback
import time
import gore

st.set_page_config(layout="wide", page_title="Gore Sim-Eye Creator")

st.write("## Create a printable simulation eye")
st.write(
    ":eye: Upload a fundus image to create a printable image that may be cut out and assembled into a simulation eye. :scissors:"
)
st.sidebar.write("## Upload and download :gear:")

# Increased file size limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Max dimensions for processing
MAX_IMAGE_SIZE = 2000  # pixels

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Convert a hex colour string to an RGBA tuple
def hex_to_rgba(hex):
  return tuple(int(hex[i:i+2], 16) for i in (1, 3, 5)) + (255,)

# Resize image while maintaining aspect ratio
def resize_image(image, max_size):
    width, height = image.size
    if width <= max_size and height <= max_size:
        return image
    
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))
    
    return image.resize((new_width, new_height), Image.LANCZOS)

def process_image(image_bytes, path):
    """Process image with caching to avoid redundant processing"""
    try:
        image = Image.open(BytesIO(image_bytes))
        # Process the image
        fixed = gore.make_rotary_adjusted(
            path, 
            gore.deg2rad(imageExtent)/2, 
            numGores, 
            gore.deg2rad(noCutExtent)/2, 
            rotation, 
            quality, 
            gore.deg2rad(retinalExtent)/2,
            background_colour=hex_to_rgba(hexColour))
        return image, fixed
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None, None

def fix_image(upload, path):
    try:
        start_time = time.time()
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        status_text.text("Loading image...")
        progress_bar.progress(10)
        
        # Read image bytes
        if isinstance(upload, str):
            # Default image path
            if not os.path.exists(upload):
                st.error(f"Default image not found at path: {upload}")
                return
            with open(upload, "rb") as f:
                image_bytes = f.read()
        else:
            # Uploaded file
            image_bytes = upload.getvalue()
        
        status_text.text("Processing image...")
        progress_bar.progress(30)
        
        # Process image (using cache if available)
        image, fixed = process_image(image_bytes, path)
        if image is None or fixed is None:
            return
        
        progress_bar.progress(80)
        status_text.text("Displaying results...")
        
        # Display images
        col1.write("Original Image :camera:")
        col1.image(image)
        
        col2.write("Gored Image :wrench:")
        col2.image(fixed)
        
        # Prepare download button
        st.sidebar.markdown("\n")
        st.sidebar.download_button(
            "Download gored image", 
            convert_image(fixed), 
            "gored.png", 
            "image/png"
        )
        
        progress_bar.progress(100)
        processing_time = time.time() - start_time
        status_text.text(f"Completed in {processing_time:.2f} seconds")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.sidebar.error("Failed to process image")
        # Log the full error for debugging
        print(f"Error in fix_image: {traceback.format_exc()}")

# UI Layout
col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Information about limitations
with st.sidebar.expander("ℹ️ Image Guidelines"):
    st.write("""
    - Image should be square with fundus tight to the edges
    - Maximum file size: 10MB
    - Supported formats: PNG, JPG, JPEG
    - Processing time depends on image size
    """)

imageExtent = st.sidebar.slider("Image extent(degrees)", min_value=10, max_value=180, value=60)

with st.sidebar.expander("More options"):
    numGores = st.slider("Number of gores", min_value=3, max_value=12, value=5)
    retinalExtent = st.slider("Retinal extent(degrees)", min_value=10, max_value=360, value = 180)
    noCutExtent = st.slider("No-cut extent(degrees)", min_value = 0, max_value = 90, value = 20)
    rotation = st.number_input("Rotation(degrees)", min_value=-180, max_value=180, value=0)
    quality = st.slider("Quality(%)", min_value = 10,max_value = 100,value=40)
    hexColour = st.color_picker("Background colour")

# Process the image
if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error(f"The uploaded file is too large. Please upload an image smaller than {MAX_FILE_SIZE/1024/1024:.1f}MB.")
    else:
        uploaded_filename = my_upload.name
        name, extension = os.path.splitext(uploaded_filename)
        temp_file = "temp" + extension
        with open(temp_file, 'wb') as fw:
            fw.write(my_upload.read())
        fix_image(upload=my_upload, path=temp_file)
else:
    # Try default images in order of preference
    default_images = ["./img1.jpg", "./img2.png"]
    for img_path in default_images:
        if os.path.exists(img_path):
            fix_image(img_path, img_path)
            break
    else:
        st.info("Please upload an image to get started!")
