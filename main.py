import os
import urllib.parse
import pyodbc
from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = '' 
server = ''
database = ''
username = ''
password = ''
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#cursor.execute("SELECT * FROM products")
#row = cursor.fetchone()

a = 0


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html", title="Home", form=search)


@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        test = request.form['test']

    global a
    a = test
        
    return render_template("index.html", title="test2", keyword=test)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        if keyword is "":
            cursor.execute("SELECT * FROM products")
        else:
            cursor.execute("SELECT * FROM products WHERE %s = '%s'" % (a, keyword))  
        rows = cursor.fetchall()
        
    count = 0
    for x in rows:
        count += 1
        print(count)
        for y in x:
            print(y)
    
    return render_template("test.html", title="test", rows=rows)

@app.route("/register", methods=['GET', 'POST'])
def register():    
    return render_template("register.html", title="Register")

@app.route("/registersubmit", methods=['GET', 'POST'])
def registersubmit():
    if request.method == 'POST':
        uid = request.form['uid']
        print(uid)
        username = request.form['username']
        print(username)
        full_name = request.form['full_name']
        birthdate = request.form['birthdate']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        role = request.form['role']
    cursor.execute("insert into users(uid, username, full_name, birthdate, email, address, password, role) values (?, ?, ?, ?, ?, ?, ?, ?)", (uid, username, full_name, birthdate, email, address, password, role))
    cnxn.commit()

    return redirect(url_for("home"))

@app.route("/order")
def order():
    return render_template("order.html")
    

@app.route("/ordersubmit", methods=['GET', 'POST'])
def ordersubmit():
    if request.method == 'POST':
        oid = request.form['oid']
        uid = request.form['uid']
        pid = request.form['pid']
        purchase = request.form['purchase']
        ship = request.form['ship']
    cursor.execute("insert into orders(oid, uid, pid, purchase, ship) values (?, ?, ?, ?, ?)", (oid, uid, pid, purchase, ship))
    cnxn.commit()
    return redirect(url_for("home"))



@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)
