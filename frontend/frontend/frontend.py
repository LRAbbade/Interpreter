from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
    return render_template('page.html')
