from flask import Flask,request,render_template,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import json
import time


app = Flask(__name__)
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tmp/user_data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class UserNetInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_action = db.Column(db.String(10))
    user_net_income =db.Column(db.String())

    def __repr__(self):
        return "<UserNetInfo {0}>".format(self.id)


@app.route("/",methods = ["GET","POST"])
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html",data="udata")

@app.route("/add/",methods = ["GET","POST"])
def addItem_to_list():
    # Validation for the fields incase JS is disabled
    if request.method == "POST":
        if request.form["income"] == "" or request.form["action-type"] == "":
            flash("Please fill in the daily income gains")
            return redirect(url_for("errorPage"))

        # add new fields here
        user_daily_income = request.form["income"]
        user_action_type  = request.form["action-type"]
        # add to db
        add_to_db(uincome = user_daily_income,uactiontype = user_action_type)
        return redirect(url_for("dashboard"))
    return "OK"

def add_to_db(uincome = None,uactiontype = None):
    user_data = UserNetInfo(user_action = uactiontype,user_net_income = uincome)
    db.session.add(user_data)
    db.session.commit()

@app.route("/error/",methods = ["GET","POST"])
def errorPage():
    return render_template("error_page.html")



if __name__ == "__main__":
    app.run(debug=True,port=5000)
