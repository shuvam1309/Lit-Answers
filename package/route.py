from package import app, mail
from flask import redirect, render_template, request, flash
from package.helper import main
from flask_login import current_user, login_user, login_required
from package.models import User

@app.route('/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/getans')
    elif request.method == "POST":
        email = request.form['mail']
        password = request.form['pass']
        user = User.query.filter_by(email = email).first()
        
        if user and user.password == password:
            if "remember" in list(request.form.keys()):
                login_user(user,request.form["remember"])
            else:
                login_user(user)
            next_page = request.args.get('next')
            flash(f"Welcome Back, {user.name.split(' ')[0]}", "success")
            return redirect(next_page) if next_page else redirect("/getans")
        else:
            flash(f"Invalid Email or Password", "danger")
    return render_template("login.html")

@app.route('/getans', methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        url = request.form['url']
        s = main(url)
        return render_template("showans.html", s = s)
    return render_template("index.html")

    


# @app.route('/getAns', methods=["GET", "POST"])
# @login_required
# def displayans(url):
#     return render_template("showans.html")