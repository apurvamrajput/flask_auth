from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required


app = Flask(__name__)

with app.app_context():
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/b37"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "jhgafet54try"

    db = SQLAlchemy(app)

    login_manager = LoginManager()#object is used to hold all settings used for logging
    login_manager.init_app(app)#to configure application for login
    login_manager.login_view = "login"  #loginview name

    class User(db.Model,UserMixin):
        id = db.Column(db.Integer,primary_key=True)
        username = db.Column(db.String(34),nullable=False)
        password = db.Column(db.String(45),nullable=False)
    db.create_all()


@app.route("/")
def database():
    return "Database Created"

@app.route("/h")
def home():
    return render_template("home.html")

@login_manager.user_loader
def load_user(user_id):
    print("called")
    return User.query.get(user_id)
    #return User.query.filter_by(id = user_id).first()# fetch the user_id in user table if user_id is present
    # it return object of specified userid if it is not present it return None

@app.route("/su",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        unm = request.form["u"]
        pwd = request.form["p"]
        obj = User(username=unm, password=pwd)
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/log" ,methods=["GET","POST"])
def login():
    if request.method=="POST":
        u = request.form.get("u")
        p = request.form.get("p")
        user = User.query.filter_by(username=u,password=p).first()#load_user function will get call
        if user:
            login_user(user)
            return redirect(url_for("final"))
    return render_template("login.html")


@app.route("/final")
@login_required
def final():
    return render_template("final.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ =="__main__":
    app.run(debug=True)