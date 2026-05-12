from flask import Flask, request, jsonify, render_template
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_landing_page():
    data = request.json
    business_name = data["business_name"]
    description = data["description"]
    audience = data["audience"]
    colour = data["colour"]

    prompt = f"""Create a complete, modern, single-page HTML landing page for a business with these details:

Business name: {business_name}
What they do: {description}
Target audience: {audience}
Colour preference: {colour}

Requirements:
- Full HTML document including all CSS in a style tag
- Modern, professional design
- Sections: hero, features/services, about, contact form (non-functional, just UI)
- Mobile responsive
- No external dependencies except Google Fonts
- Return ONLY the raw HTML code, no explanation, no markdown, no code blocks"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return jsonify({"html": message.content[0].text})

if __name__ == "__main__":
    app.run(debug=True)