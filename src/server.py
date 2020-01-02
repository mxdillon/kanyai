from flask import request, render_template, jsonify


def health_route():
    return jsonify({"Status": 'OK'})


def index_route():
    if request.method == 'GET':

        text_input = request.args.get('text_input')
        if text_input is None:
            text_input = ""

        if len(text_input) > 0:
            result = ' '.join([text_input for t in range(100)])
        else:
            result = ""

        return render_template('index.html', text_input=text_input,
                               result=result)

    return render_template('index.html')
