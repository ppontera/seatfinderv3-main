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
    user_id = data.get('user_id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({'error': 'Missing user_id or password'}), 400

    if check_credentials(user_id, password):
        session['userID'] = user_id  # Set session variable
        return redirect(url_for('static', filename='home.html'))
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

def connect_to_database():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def check_credentials(user_id, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
    cursor.execute(query, (user_id, password))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == '__main__':
    app.run(debug=True)
