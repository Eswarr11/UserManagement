from flask import Flask,render_template, request,url_for,redirect,flash
from flask_mysqldb import MySQL
app=Flask(__name__)
#database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'
app.config['MYSQL_CURSORCLASS']="DictCursor"
mysql=MySQL(app)

#Loading home page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

#New User
@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con = mysql.connection.cursor()
        sql="insert into users(name,CITY,AGE) value(%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close
        flash('User details added')
        return redirect(url_for("home"))
    return render_template("addusers.html")
#update user
@app.route("/editUser/<string:id>",methods=['GET','POST'])
def editusers(id):
    con = mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update users set name=%s,CITY=%s,AGE=%s where id=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        flash('User details updated')
        return redirect(url_for("home"))
    sql='select * from users where ID=%s'
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editusers.html",datas=res)
#delete user
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteuser(id):
    con = mysql.connection.cursor()
    sql = "delete from users where id=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close
    flash('User details deleted')
    return redirect(url_for("home"))
if(__name__ == '__main__'):
    app.secret_key="abc123"
    app.run(host="0.0.0.0",use_reloader=True ,debug=True)