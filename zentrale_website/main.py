from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def homepage():
    return render_template("index.html")

def start_website(debug=False):
    app.run(debug=debug)

if __name__ == '__main__':
    # debug can only be enabled when running the file directly
    # cause it throws an error if you try to do it while in threads
    start_website(True)
