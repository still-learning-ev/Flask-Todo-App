from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')

def hello_world():
    return "Hello world"

@app.route('/json')
def jsonFunction():
    return {"name":"hello", "game":"something"}


@app.route('/renderhtml')
def renderhtml():
    return render_template('index.html')
if __name__=="__main__":
    app.run(debug=True, port=5000)