from flask import Flask, g
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL , MySQLdb
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
print(secrets.token_hex(16))
# Database configuration
"""db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'club_management',
    'buffered': True,
}
"""
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'club_management'

mysql = MySQL(app)
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def index():
    return 'success ll home'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        # Get data from the form
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        dob = request.form['dob'] #dob = date of birth
        discord = request.form['discord']
        email = request.form['email']
        password = request.form['password']
        school_year = request.form['school_year']
        university = request.form['university']
        skills = request.form['skills']
        departement = request.form['departement']

        # Insert data into the Member table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Member (fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # i use DictCursor to retreive the table tuple in form of dictionory
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Member WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # use session for the after login process
            session['member_id'] = user['memberID']
            session['member_email'] = user['email']
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('member_id', None)
    session.pop('member_email', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home_manager.html')

if __name__ == '__main__':
    app.run(debug=True)
