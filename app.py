from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # لإدارة الجلسات

# MySQL Configuration
db_config = {
    'user': 'root',
    'password': '12345678',
    'host': '127.0.0.1',
    'database': 'electric_cars'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and user['password'] == password:
        session['username'] = username  # حفظ اسم المستخدم في الجلسة
        return redirect(url_for('home'))
    else:
        return redirect(url_for('error'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        session['username'] = username  # حفظ اسم المستخدم في الجلسة
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/select_option', methods=['GET', 'POST'])
def select_option():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        option = request.form['option']
        date = request.form['date']
        revenue = request.form['revenue']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if option == 'tesla':
            cursor.execute('INSERT INTO tesla_revenue (date, revenue) VALUES (%s, %s)', (date, revenue))
        elif option == 'byd':
            cursor.execute('INSERT INTO byd_revenue (date, revenue) VALUES (%s, %s)', (date, revenue))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('home'))
    
    return render_template('select_option.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # إزالة اسم المستخدم من الجلسة
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
