from flask import Flask, request, jsonify
import psycopg2

app = Flask("Backend for HTTP Requests")

# Database connection configuration
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = '1234'

def create_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection

# HEAD method to check if the server is running
@app.route('/users', methods=['HEAD'])
def ping():
    print(request.headers)
    return jsonify({'message': 'Server is running'})


# GET method to retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    print(request.headers)
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email FROM Users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

# POST method to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (name, email) VALUES (%s, %s)", (name, email))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User created'})

# PUT method to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    print(request.headers)
    data = request.get_json()
    name = data['name']
    email = data['email']
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    connection.commit()

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({'error': 'User not found'}), 404

    cursor.close()
    connection.close()
    return jsonify({'message': 'User updated', 'id': user_id})

# DELETE method to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Users WHERE id = %s", (user_id,))
    connection.commit()

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({'error': 'User not found'}), 404

    cursor.close()
    connection.close()
    return jsonify({'message': 'User deleted', 'id': user_id})


if __name__ == '__main__':
    app.run()
