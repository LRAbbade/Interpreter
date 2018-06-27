from flask import render_template, Flask, request
import interpreter

app = Flask(__name__)
interpreter.main()

@app.route('/', methods=['GET', 'POST'])
def root():
    context = {
        'dados':interpreter.get_dados(),
        'registradores':interpreter.get_registradores(),
        'cache':interpreter.get_cache(),
        'cache_dec':interpreter.get_cache_decimal(),
        'cache_size':interpreter.cache_size,
        'original_instruction':None
    }

    if request.method == 'POST':
        if 'instruction' in request.form:
            command = {
                'instruction':request.form['instruction'],
                'register_1':request.form['register_1'],
                'register_2':request.form['register_2']
            }

            interpreter.execute(**command)
            context['original_instruction'] = command
            context['cache_dec'] = interpreter.get_cache_decimal()
        elif 'load' in request.form:
            interpreter.update_dados([
                request.form['D0'],
                request.form['D1'],
                request.form['D2'],
                request.form['D3'],
                request.form['D4'],
                request.form['D5'],
                request.form['D6'],
                request.form['D7']
            ])

            context['dados'] = interpreter.get_dados()
        elif 'save' in request.form:
            interpreter.save_dados()
        else:
            print('Invalid post request')

        return render_template('page.html', **context)
    else:
        return render_template('page.html', **context)
