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
        query = """
    INSERT INTO Member (
        fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT departementName FROM Departement WHERE departementName = %s)
    )
"""
        cur.execute(query, (fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Member WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # use session for the after login process
            session['member_id'] = user['memberID']
            session['member_email'] = user['email']
            if user['role'] == 'Manager':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('user_home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('member_id', None)
    session.pop('member_email', None)
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    
    if 'member_id' not in session:
        return redirect(url_for('login'))
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Member WHERE memberID = %s", (session['member_id'],))
        user = cur.fetchone()
        #count the total number of users 
        cur.execute("SELECT COUNT(*) AS user_count FROM Member")
        user_count = cur.fetchone()['user_count']
        #the percentage 
        total_users = 250 #retrive it from discord server
        registration_percentage = (user_count / total_users) * 100
        #count the total number of events
        cur.execute("SELECT COUNT(*) AS event_count FROM club_event")
        event_count = cur.fetchone()['event_count']
        #count the total number of events
        cur.execute("SELECT COUNT(*) AS dep_count FROM departement")
        dep_count = cur.fetchone()['dep_count']
        #count the total count of members across all events
        cur.execute("SELECT COUNT(DISTINCT m.memberID) AS event_members_count FROM club_event c JOIN participate p ON p.id_event = c.id_event JOIN member m ON m.memberID = p.member_id;")
        event_members_count = cur.fetchone()['event_members_count']
        #the percentage
        active_member_percentage = ( event_members_count / user_count) * 100
        cur.close()
        return render_template(
            'home_manager.html',
            user=user,
            user_count=user_count,
            registration_percentage = registration_percentage,
            event_count=event_count,
            dep_count= dep_count,
            event_members_count= event_members_count,
            active_member_percentage = active_member_percentage)
@app.route('/home')
def user_home():
    if 'member_id' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('home_user.html')
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'member_id' not in session:
        return redirect(url_for('login'))
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Member WHERE memberID = %s", (session['member_id'],))
        user = cur.fetchone()
        print("parttttttttt one")
        if request.method == 'POST':
            print("it workkkkkkkkkkkkkkkkkkkkkkkkk")
            new_email = request.form['editEmail']
            new_discord = request.form['editDiscord']
            new_skills = request.form['editSkills']
            new_departement = request.form['editDepartement']
            
            cur = mysql.connection.cursor()
            query = """
                UPDATE Member
                SET email = %s, discord = %s, skills = %s, departement = (SELECT departementName FROM Departement WHERE departementName = %s)
                WHERE memberID = %s
            """
            cur.execute(query, (new_email, new_discord, new_skills, new_departement, session['member_id']))


            mysql.connection.commit()
            cur.close()
            return render_template(
            'user_profile.html', user = user)
        cur.close()
        return render_template(
            'user_profile.html',user = user)

@app.route('/delete_user', methods=['POST', 'DELETE'])
def delete_user_profile():
    print('yes mechat')
    if 'member_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.form['_method'] == 'DELETE':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Member WHERE memberID = %s", (session['member_id'],))
            mysql.connection.commit()
            cur.close()
            session.clear()  
            return redirect(url_for('login'))
        else:
            return 'there are error try again'
        
if __name__ == '__main__':
    app.run(debug=True)
