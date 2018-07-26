from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("form.html")

@app.route("/process", methods=['POST'])
def process():

    email = request.form['email']
    name = request.form['name']

    if name and email:
        newName = name[::-1]

        return jsonify({'name' : newName})

    return jsonify({'error' : 'Missing data!'})


if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)