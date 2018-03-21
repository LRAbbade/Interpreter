from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
    return render_template('page.html')

# dar um jeito de pegar a action do form
@app.route('/run?<int:instruction>&<int:register_1>&<int:register_2>')
def show_post(instruction, register_1, register_2):
    print(instruction, register_1, register_2)
