from flask import Flask, request, render_template

app = Flask(__name__)


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
    app.run(port=5001)
