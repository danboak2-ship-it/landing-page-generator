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

    prompt = f"""Create a stunning, modern, production-quality single-page HTML landing page for a business with these details:

Business name: {business_name}
What they do: {description}
Target audience: {audience}
Colour preference: {colour}

Design requirements:
- Bold, memorable design — NOT generic or template-looking
- Smooth scroll animations using Intersection Observer API (elements fade/slide in as you scroll)
- Hero section with animated gradient background or mesh gradient
- Glassmorphism cards for features/services section
- Smooth hover effects on all buttons and cards (transform, box-shadow transitions)
- Sticky navbar that changes style on scroll
- Animated counter numbers in a stats section (e.g. "500+ clients", "10 years experience")
- Testimonials section with styled quote cards
- Contact section with a styled form
- Subtle floating/parallax elements in the hero
- Custom CSS animations (keyframes) for hero elements fading in on load
- Mobile responsive with hamburger menu
- Google Fonts — use a distinctive font pairing, NOT Arial or Roboto
- Colour scheme based on preference: {colour}
- Footer with links

Technical requirements:
- Everything in one HTML file — all CSS in style tags, all JS in script tags
- No external dependencies except Google Fonts
- Use CSS custom properties (variables) for colours
- Intersection Observer for scroll animations
- Clean, semantic HTML structure

Return ONLY the raw HTML code. No explanation, no markdown, no code blocks. Start with <!DOCTYPE html>"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    html_content = message.content[0].text
    print(f"HTML length: {len(html_content)} characters")
    print(f"HTML ends with: {html_content[-100:]}")
    return jsonify({"html": html_content})

if __name__ == "__main__":
    app.run(debug=True)