from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key_here"

# ✅ MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="09871",
    database="user_management",
    autocommit=True  # Important to commit insertions without db.commit()
)
cursor = db.cursor()

@app.route('/')
def home():
    return redirect('/login')

# ✅ LOGIN route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['email'] = email
            return redirect('/portfolio')
        else:
            return "Invalid Email or Password"
    return render_template("login.html")

# ✅ SIGNUP route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            return redirect('/login')
        except mysql.connector.Error as err:
            return f"Error: {err}"
    return render_template("signup.html")

# ✅ Portfolio (after login)
@app.route('/portfolio')
def portfolio():
    if 'email' in session:
        return render_template("portfolio.html", email=session['email'])
    return redirect('/login')

# ✅ Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
