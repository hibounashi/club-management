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
        dob = request.form['dob']  # dob = date of birth
        discord = request.form['discord']
        email = request.form['email']
        password = request.form['password']
        school_year = request.form['school_year']
        university = request.form['university']
        skills = request.form['skills']
        departement_name = request.form['departement']  # Change to departement_name

        # Get the departementID corresponding to the departementName
        cur = mysql.connection.cursor()
        cur.execute("SELECT departementID FROM Departement WHERE departementName = %s", (departement_name,))
        departement_row = cur.fetchone()
        if departement_row:
            departement_id = departement_row[0]
        else:
            # Handle case where departementName doesn't exist
            # You may want to redirect to an error page or provide an error message
            return "Error: Departement not found"

        # Insert data into the Member table
        query = """
            INSERT INTO Member (
                fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        cur.execute(query, (fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement_id))
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
        total_users = 50 #retrive it from discord server
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
@app.route('/home', methods=['GET', 'POST'])
def user_home():
    if 'member_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            success = None
            member_id = session['member_id']
            
            event_name = request.form['event_name']
            #event_description = request.form.get('event_description')  # Optional
            
            # Initialize event_id variable
            event_id = None
            
            # Check if the event already exists
            cur = mysql.connection.cursor()
            cur.execute("SELECT id_event FROM club_event WHERE eventName = %s", (event_name.encode('utf-8'),))
            existing_event = cur.fetchone()
            
            if existing_event:
                # If event exists, get its ID
                event_id = existing_event[0]
            else:
                # If event doesn't exist, insert it into the club_event table
                cur.execute("INSERT INTO club_event (eventName) VALUES (%s)", (event_name,))
                mysql.connection.commit()
                event_id = cur.lastrowid  # Get the ID of the newly inserted event
            
            # Add participation entry for the member in the event if event_id is not None
            if event_id:
                cur.execute("INSERT INTO participate (member_id, id_event) VALUES (%s, %s)", (member_id, event_id))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('user_home', success=True)) 
            else:
                return redirect(url_for('user_home', success=False))
        return render_template('home_user.html', success=request.args.get('success'))

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
@app.route('/profile_user', methods=['GET', 'POST'])
def profile_user():
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
            'userprofile.html', user = user)
        cur.close()
        return render_template(
            'userprofile.html',user = user)
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

@app.route('/event_management', methods=['GET', 'POST'])
def event_management():
    if 'member_id' not in session:
        return redirect(url_for('login'))
    else:
        # Fetch events from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_event, eventName FROM club_event")
        events = cur.fetchall()
        
        # Fetch participants for each event
        participants = {}
        for event in events:
            cur.execute("SELECT member.fname, member.lname "
                        "FROM participate "
                        "JOIN member ON participate.member_id = member.memberID "
                        "WHERE participate.id_event = %s", (event[0],))
            participant_names = cur.fetchall()  # Fetch names of participants for the current event
            participants[event[1]] = [f"{participant[0]} {participant[1]}" for participant in participant_names]
        
        cur.close()
        return render_template('event.html', events=events, participants=participants)

if __name__ == '__main__':
    app.run(debug=True)
