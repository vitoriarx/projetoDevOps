from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_connection():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

# ----------------- CRUD DE USUÁRIOS -----------------

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (data['name'], data['email']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Usuário adicionado com sucesso!"})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s;", (data['name'], data['email'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Usuário atualizado com sucesso!"})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Usuário deletado com sucesso!"})


# ----------------- CRUD DE PRODUTOS -----------------

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products;")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s);",
        (data['name'], data['price'], data['stock'])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Produto adicionado com sucesso!"})

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s;",
        (data['name'], data['price'], data['stock'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Produto atualizado com sucesso!"})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Produto deletado com sucesso!"})


# ----------------- MAIN -----------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
