from flask import Flask, render_template
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')

URL = 'https://api.nasa.gov/planetary/apod'
API_KEY = os.getenv('NASA_KEY')

parameters = {
    "api_key": API_KEY,
}


def is_image_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            img = Image.open(BytesIO(response.content))
            img.verify()  # Verify if the content is an image
            return True
        except (IOError, SyntaxError):
            pass
    return False


@app.route("/")
def home():
    try:
        response = requests.get(url=URL, params=parameters)
        response.raise_for_status()
        data = response.json()
        apod_title = data['title']
        apod_date = data['date']
        apod_explanation = data['explanation']
        if is_image_url(data['url']):
            img_url = data['url']
        else:
            img_url = "https://api.nasa.gov/assets/img/general/apod.jpg"

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
    return render_template("index.html", title=apod_title,
                           explanation=apod_explanation, date=apod_date, url=img_url)


if __name__ == "__main__":
    app.run(debug=True)
