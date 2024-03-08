from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key_here" 

mydb = mysql.connector.connect(
    host='127.0.0.1', 
    user='root',  
    password='VamsKris@987',
    database='foxsense'
)
mycursor = mydb.cursor(buffered=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        mycursor.execute("SELECT * FROM login WHERE username = %s AND passw = %s", (username, password))
        user = mycursor.fetchone()
        if user:
            session['userid'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('profile'))
        else:
            error = "Incorrect username or password. Please try again."
            return render_template('home.html', error=error)
    return render_template('home.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        userid = session['userid']
        return render_template('profile.html', username=username, userid=userid)
    else:
        return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        department = request.form['department']
        salary = request.form['salary']

        try:
            mycursor.execute("INSERT INTO login (userid, username, passw, age, department, salary) VALUES (%s, %s, %s, %s, %s, %s)", (userid, username, password, age, department, salary))
            mydb.commit()
            return redirect(url_for('home'))
        except mysql.connector.IntegrityError as e:
            error = "Username already exists. Please choose a different one."
            return render_template('signup.html', error=error)
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
