from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jenny1212'
app.config['MYSQL_DB'] = 'login_info'
app.config['SECRET_KEY'] = os.urandom(30)

mysql = MySQL(app)


@app.route('/', methods=["GET"])
def home():
    return render_template("sign_in.html")



#Sign Up page starts here-----
@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
    
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO login_cre(username,fullname,email,password) VALUES (%s,%s,%s,%s)', (username,fullname,email,password))
        cur.execute('INSERT INTO login_access(username, password ) VALUES (%s,%s)',(username,password))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('sign_in'))
   
    return render_template('sign_up.html')






#Sign in page starts here-----
@app.route('/sign_in', methods = ['GET','POST'])
def sign_in():
    if request.method == 'POST':

        email = request.form['email'] 
        password = request.form['password']
                
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM login_cre WHERE email = %s AND password = %s',(email, password))
        user = cur.fetchall()


        if user:
            print(user)
            session["user_name"] = user[0][0]
            data = session.get("user_name")
            print(data)
            return redirect(url_for('dashboard'))
        
    return render_template('sign_in.html')





@app.route('/dashboard', methods=["GET"])
def dashboard():
    user_id = session.get("user_name")
    if user_id:
        print(user_id)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * from login_cre WHERE user_id = %s", (user_id,))
        data = cur.fetchall()
        print(data)
        cur.execute("SELECT * from login_cre")
        contact_data = cur.fetchall()
        return render_template("dashboard.html", data = data, contact_data = contact_data)
    else:
        return redirect('sign_in')

@app.route('/dashboard_contact/<int:id>', methods = ['GET'])
def dashboard_contact(id):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * from login_cre WHERE user_id = %s", (id,))
    data = cur.fetchall()
    print(data)
    cur.execute("SELECT fullname from login_cre")
    contact_data = cur.fetchall()
    return render_template("dashboard_contact.html", data = data, contact_data = contact_data)




@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
  cur = mysql.connection.cursor()
  if request.method == "POST":  # 
    fullname = request.form['fullname']
    email = request.form['email']
    number = request.form['number']
    cur.execute("UPDATE login_cre SET fullname = %s, email= %s, mob_num = %s WHERE user_id = %s",(fullname, email, number, id))  # Update SQL command
    mysql.connection.commit()  
    mysql.connection.close 
    return redirect(url_for("dashboard"))  # Go to dashboard
  cur.execute("SELECT * FROM login_cre WHERE user_id = %s", (id, ))
  data = cur.fetchall()
  return render_template('update.html', data=data)


@app.route("/delete/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()                                     
    cur.execute('DELETE FROM login_cre WHERE user_id = %s ', (id,))      
    mysql.connection.commit()                                           
    return redirect(url_for('dashboard'))      

@app.route('/logout')
def logout():
    session.clear()
    id = session.get('user_id')
    print('logout')
    print(id)
    return redirect('sign_in')

@app.route('/dashboard_add', methods = ['GET','POST'])
def dashboard_add():

    if request.method == "POST":
        fullname = request.form['fullname']
        email = request.form['email']
        number = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO login_cre(fullname,email,mob_num) VALUES (%s,%s,%s)', (fullname,email,number))
        
        mysql.connection.commit()
        cur.close()
        
        return redirect('dashboard')
    
    return render_template('dashboard_add.html')

app.run(debug=True)