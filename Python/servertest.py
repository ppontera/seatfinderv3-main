from flask import Flask, request, jsonify, session, redirect, url_for
import pymysql

app = Flask(__name__, static_url_path='', static_folder='../HTML')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# MySQL Configuration
DB_HOST = '107.180.1.16'
DB_USER = 'spring2024Cteam9'
DB_PASSWORD = 'spring2024Cteam9'
DB_NAME = 'spring2024Cteam9'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('home.html')
    
    # The POST request handling
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    # Check credentials
    user = check_credentials(username, password)
    if user:
        session['username'] = username  # Set session variable
        # Check if user is admin
        if is_admin(username):
            return jsonify({'isAdmin': True}), 200
        else:
            return jsonify({'isAdmin': False}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

def is_admin(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    # Execute the SQL query to check if the user is an admin
    sql = "SELECT admin FROM users WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        return True
    else:
        return False

def connect_to_database():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def check_credentials(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == '__main__':
    app.run(debug=True)
