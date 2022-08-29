
from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder='./app')
    
@app.route("/main")
def main():
    return render_template('main.html')
                
@app.route("/")
def index():
    return render_template('index.html')
                