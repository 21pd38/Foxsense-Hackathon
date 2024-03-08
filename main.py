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
            return redirect(url_for('profile'))  # Redirect to profile page after successful login
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

@app.route('/register_campus', methods=['GET', 'POST'])
def register_campus():
    if request.method == 'POST':
        campus_id = request.form['campus_id']
        campus_name = request.form['campus_name']
        try:
            mycursor.execute("INSERT INTO Campus (campusID, name) VALUES (%s, %s)", (campus_id, campus_name))
            mydb.commit()
            return redirect(url_for('home'))
        except mysql.connector.Error as e:
            error = "Error occurred while registering campus."
            return render_template('register_campus.html', error=error)
    return render_template('register_campus.html')


@app.route('/register_cafe', methods=['GET', 'POST'])
def register_cafe():
    if request.method == 'POST':
        campus_id = request.form['campus_id']
        cafe_id = request.form['cafe_id']
        cafe_name = request.form['cafe_name']
        try:
            mycursor.execute("INSERT INTO Cafe (campusID, cafeID, name) VALUES (%s, %s, %s)", (campus_id, cafe_id, cafe_name))
            mydb.commit()
            return redirect(url_for('home'))
        except mysql.connector.Error as e:
            error = "Error occurred while registering cafe."
            return render_template('register_cafe.html', error=error)
    return render_template('register_cafe.html')

@app.route('/register_item', methods=['GET', 'POST'])
def register_item():
    if request.method == 'POST':
        item_id = request.form['item_id']
        campus_id = request.form['campus_id']
        cafe_id = request.form['cafe_id']
        item_name = request.form['item_name']
        description = request.form['description']
        price = request.form['price']
        dietary_info = request.form['dietary_info']
        try:
            mycursor.execute("INSERT INTO MenuItem (itemID, campusID, cafeID, itemName, description, price, dietaryInfo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (item_id, campus_id, cafe_id, item_name, description, price, dietary_info))
            mydb.commit()
            return redirect(url_for('home'))
        except mysql.connector.Error as e:
            error = "Error occurred while registering item."
            return render_template('register_item.html', error=error)
    return render_template('register_item.html')

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        user_id = request.form['user_id']
        campus_id = request.form['campus_id']
        cafe_id = request.form['cafe_id']
        item_ids = request.form['item_ids'] 

        try:
            sql = "INSERT INTO Order_Place (userID, campusID, cafeID, itemIDs) VALUES (%s, %s, %s, %s)"
            mycursor.execute(sql, (user_id, campus_id, cafe_id, item_ids))
            mydb.commit()

            return redirect(url_for('home')) 
        except mysql.connector.Error as e:
            error = "Error occurred while placing the order."
            return render_template('place_order.html', error=error)

    return render_template('place_order.html')


if __name__ == '__main__':
    app.run(debug=True)
