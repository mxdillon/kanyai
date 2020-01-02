from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def create_app():
    """ Create the Flask application"""
    return app


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"Status": 'OK'})


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':

        text_input = request.args.get('text_input')
        if text_input is None:
            text_input = ""

        if len(text_input) > 0:
            result = ' '.join([text_input for t in range(100)])
        else:
            result = ""

        return render_template(r'index.html', text_input=text_input,
                               result=result)

    return render_template('/index.html')


if __name__ == "__main__":
    app.run()
