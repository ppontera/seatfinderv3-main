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

    if check_credentials(username, password):
        session['username'] = username  # Set session variable
        return redirect(url_for('static', filename='home.html'))
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

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

 # create account server integration 
 
@app.route('/createAccount', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # Consider hashing this password
    email = data.get('email')

    # Insert data into database
    success = insert_new_user(username, password, email)

    if success:
        return jsonify({"message": "Account created successfully"}), 200
    else:
        return jsonify({"error": "Failed to create account"}), 500

def insert_new_user(username, password, email, admin=0, degree=''):
    conn = connect_to_database()
    try:
        cursor = conn.cursor()
        # Assuming 'created_at' defaults to the current timestamp automatically by the database
        # and 'admin' is a flag that you might want to set as part of the function call,
        # and 'degree' can be an optional parameter.
        query = "INSERT INTO users (username, password, email, admin, degree) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (username, password, email, admin, degree))
        conn.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if conn:
            conn.close()



if __name__ == '__main__':
    app.run(debug=True)
