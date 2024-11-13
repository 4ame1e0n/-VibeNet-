from flask import Flask, render_template, url_for, request, redirect, session, make_response

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)



@app.route('/')

@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page:" + name + "-" + str(id)

if __name__ == "__main__":
        app.run(debug=True)
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
        #socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

