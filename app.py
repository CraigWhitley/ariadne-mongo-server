from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv("MONGO_URL")
}


db = MongoEngine(app)


@app.route('/')
def index():
    return '<h1> Hello, World </h1>'


if(__name__) == '__main__':
    app.run()
