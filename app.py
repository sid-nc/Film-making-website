# Import necessary modules
from flask import Flask, render_template, request
import requests
import io
from PIL import Image
import google.generativeai as genai

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

# Initialize Flask app
app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key="AIzaSyA0vLcQ5gkmkC0Qf8uvFJARecC9QjA_O2c")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Define route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define route for the image generation page
@app.route('/generate_image', methods=['GET', 'POST'])
def generate_image():
    if request.method == 'POST':
        # Get user input from the form
        prompt = request.form['prompt']
        
        # Generate output using the model
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        image_bytes = response.content
        
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_bytes))
        image.show()
        
        return render_template('generate_image.html')
    else:
        return render_template('generate_image.html')
    
@app.route('/script_generation_page', methods=['GET', 'POST'])
def script_generation_page():
    if request.method == 'POST':
        # Get user input from the form
        logline = request.form['logline']
        
        # Generate output using the model
        convo = model.start_chat(history=[])
        convo.send_message(logline)
        output = convo.last.text
        
        # Render the output template with the generated text
        return render_template('output.html', output=output)
    else:
        return render_template('script_generation_page.html')

@app.route('/previous_page')
def previous_page():
    return render_template('previous_page.html')


if __name__ == '__main__':
    app.run(debug=True)
