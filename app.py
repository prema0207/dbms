from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from generate_certificate import create_pdf
import config

app = Flask(__name__)
app.secret_key = 'secret'

# MySQL Configuration
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        mysql.connection.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect('/apply')
    return render_template('login.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        cert_type = request.form['type']
        income = request.form['income']
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO applications (user_id, cert_type, income, status) VALUES (%s, %s, %s, %s)",
                       (user_id, cert_type, income, 'Pending'))
        mysql.connection.commit()
        return redirect('/')
    return render_template('apply.html')

@app.route('/admin')
def admin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT a.id, u.name, a.cert_type, a.income, a.status FROM applications a JOIN users u ON a.user_id = u.id")
    data = cursor.fetchall()
    return render_template('admin.html', apps=data)

@app.route('/admin/approve/<int:app_id>')
def approve(app_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT a.*, u.name FROM applications a JOIN users u ON a.user_id = u.id WHERE a.id = %s", (app_id,))
    app_data = cursor.fetchone()
    create_pdf(app_data)
    cursor.execute("UPDATE applications SET status='Approved' WHERE id = %s", (app_id,))
    mysql.connection.commit()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
