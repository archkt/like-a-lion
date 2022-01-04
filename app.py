from flask import *

app = Flask(__name__)
app.secret_key = "test"

@app.route('/')
def index():
    # TODO:
    # enable session to modify the login_status

    login_status = "login" in session and session["login"] == 'true'
    print(login_status)
    if login_status:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login_status = request.form["login"]
        session["login"] = login_status
        return redirect(url_for('index'))
    else:
        login_status = "login" in session and session["login"] == 'true'
        if login_status:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)