import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyBPMPRFS7FlYfZ6VyZtcX6Sz-AoolBuIZI")

def generate_layout_from_image(image_path, screen_name):
    prompt = f"""You are an expert Android UI developer.
This is a screenshot of a mobile app screen: "{screen_name}".
Generate only the layout XML using ConstraintLayout.
Include proper ids, views (TextView, ImageView, Button), styling, and placeholder images.
Only return valid XML."""
    
    image = Image.open(image_path)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content([prompt, image])
    return response.text
