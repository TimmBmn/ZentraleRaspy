from flask import Flask, render_template

# only serve on static page
app = Flask(__name__)
@app.route("/")
def hello_world():
    return render_template("index.html")

def start_website():
    app.run()
    # app.run(debug=True)

if __name__ == '__main__':
    start_website()
