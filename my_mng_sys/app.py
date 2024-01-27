from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/club_management'# Replace with your MySQL database URI
db = SQLAlchemy(app)

class Member(db.Model):
    memberID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    memeberName = db.Column(db.String(50))
    memeberLastName = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    gender = db.Column(db.String(20))
    discord_id = db.Column(db.String(20))
    Dob = db.Column(db.Date)
    password = db.Column(db.String(255), nullable=False)
    yearOfStudy = db.Column(db.String(10))
    departement = db.Column(db.String(50))
    university = db.Column(db.String(50))
    skills = db.Column(db.String(50))
    confirmpassword = db.Column(db.String(20))

def calculate_age(dob):
    # Convert the date of birth string to a datetime object
    dob_date = datetime.strptime(str(dob), '%Y-%m-%d')

    # Get the current date
    current_date = datetime.now()

    # Calculate the age
    age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))

    return age

@app.route('/')
def home():
    # Use a custom SQL query to retrieve member data
    sql_query = text("""
        SELECT * FROM Member
    """)
    result = db.session.execute(sql_query)  # Use db.session.execute instead of db.engine.execute
    
    # Fetch all rows as a list of tuples
    rows = result.fetchall()

    # Get the column names from the result object
    columns = result.keys()

    # Convert rows to dictionaries
    members = [dict(zip(columns, row)) for row in rows]

    # Pass the members data and the calculate_age function to the template
    return render_template('home.html', members=members, calculate_age=calculate_age)



@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        gender = request.form['gender']
        discord_id = request.form['discord']
        dob = request.form['dob']
        password = request.form['password']
        school_year = request.form['school_year']
        departement = request.form['departement']
        university = request.form['university']
        skills = request.form['skills']
        confirmpassword = request.form['confirmpassword']

        # SQL query to insert data into the Member table
        sql_query = text("""
            INSERT INTO Member (memeberName, memeberLastName, email, gender, discord_id, Dob, password, yearOfStudy, departement, university, skills, confirmpassword)
            VALUES (:fname, :lname, :email, :gender, :discord, :dob, :password, :school_year, :departement, :university, :skills, :confirmpassword)
        """)
        
        db.session.execute(sql_query, {
            'fname': fname,
            'lname': lname,
            'email': email,
            'gender': gender,
            'discord': discord_id,
            'dob': dob,
            'password': password,
            'school_year': school_year,
            'departement': departement,
            'university': university,
            'skills': skills,
            'confirmpassword': confirmpassword,
        })
        db.session.commit()
        #return redirect(url_for('home'))
    return render_template('signup.html')


@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(debug=True)


