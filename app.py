from flask import Flask, render_template, request
import openai
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    result2 = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = openai.responses.create(
                model="gpt-4.1",  
                input=[{"role": "developer", "content": "You are a dream interpreter. Your job is to analyze and deconstruct the dreams given through the prompts. Respond to the user by describing what you think their dreams are trying to tell them about their own unconcisous. Use Jungian psychology terms like persona, shadow, archetype. "}, 
                          {"role": "user", "content": prompt}],
                          temperature=1.4,
                          max_output_tokens=50
            )
            result = response.output_text
        except Exception as e:
            result = f"Error: {str(e)}"

        try:
            response2 = openai.images.generate(
                model="gpt-image-1-mini",  
                prompt=prompt,
                quality="medium"
            )
            image_bytes = base64.b64decode(response2.data[0].b64_json)
            with open("output.png", "wb") as f:
                f.write(image_bytes)

        except Exception as e:
            result2 = f"Error: {str(e)}"
            
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing