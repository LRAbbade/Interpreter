from flask import render_template, Flask, request
import interpreter

app = Flask(__name__)
interpreter.main()

@app.route('/', methods=['GET', 'POST'])
def root():

    context = {
        'dados':interpreter.dados,
        'registradores':interpreter.registradores,
        'original_instruction':None
    }

    if request.method == 'POST':
        if request.form['instruction'] is not None:
            command = {
                'instruction':request.form['instruction'],
                'register_1':request.form['register_1'],
                'register_2':request.form['register_2']
            }

            interpreter.execute(**command)

            context['original_instruction'] = command
        elif request.form['D0'] is not None:
            interpreter.dados = [
                request.form['D0'],
                request.form['D1'],
                request.form['D2'],
                request.form['D3'],
                request.form['D4'],
                request.form['D5'],
                request.form['D6'],
                request.form['D7']
            ]

            context['dados'] = interpreter.dados
        else:
            interpreter.save_dados()

        return render_template('page.html', **context)
    else:
        return render_template('page.html', **context)
