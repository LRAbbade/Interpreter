from flask import render_template, Flask, request
app = Flask(__name__)

@app.route('/')
def root():
    return render_template('page.html')

# exemplo de como pegar as infos do form e postar em outro html
# arrumar agora pra usar o comando em main.py e printar o resultado em run.html
@app.route('/run', methods=['POST'])
def show_post():
    context = {
        'instruction':request.form['instruction'],
        'register_1':request.form['register_1'],
        'register_2':request.form['register_2']
    }
    return render_template('run.html', **context)
