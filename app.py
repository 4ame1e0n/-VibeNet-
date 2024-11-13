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

@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return redirect(url_for("register_user", error="Passwords do not match!"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose a different username.", 'error')
            return redirect(url_for("register_user", error="Already registered!"))

        hashed_password = generate_password_hash(password1, method='pbkdf2:sha1')

        new_user = User(username=username, name=name, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('login')
        except Exception as e:
            app.logger.error(f"Error while registering: {str(e)}")

    else:
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']
        remember_me = 'remember' in request.form

        user = db.session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["authenticated"] = True
            session["id"] = user.id
            session["username"] = user.username

            remember_me = 'remember' in request.form

            if remember_me:
                resp = make_response(redirect(url_for('dashboard')))
                resp.set_cookie('remember_me', '1', max_age=365 * 24 * 60 * 60)
                return resp
            return redirect('/posts')
        else:
            flash('Username or password incorrect. Please try again.', 'error')
            return redirect('/login')


    return render_template("login.html", context=None)










if __name__ == "__main__":
        app.run(debug=True)
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
        #socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

