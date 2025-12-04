from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Variáveis de ambiente corretas de acordo com o docker-compose
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")   # <<< CORRIGIDO

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# ------------------------
# ROTA RAIZ — compatível com test_main.py
# ------------------------
@app.route('/')
def home():
    return jsonify({"message": "API funcionando!"})   # <<< CORRIGIDO

# ------------------------
# CRUD DE USUÁRIOS
# ------------------------

# LISTAR TODOS OS USUÁRIOS
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users;")
        users = cur.fetchall()

        users_list = [
            {"id": u[0], "name": u[1], "email": u[2]}
            for u in users
        ]

        cur.close()
        conn.close()
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CRIAR USUÁRIO
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Nome e email são obrigatórios"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
            (name, email)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"id": user_id, "name": name, "email": email}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ATUALIZAR USUÁRIO
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    email = data.get("email")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id;",
            (name, email, user_id)
        )

        if cur.rowcount == 0:
            return jsonify({"error": "Usuário não encontrado"}), 404

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Usuário atualizado com sucesso"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETAR USUÁRIO
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))

        if cur.rowcount == 0:
            return jsonify({"error": "Usuário não encontrado"}), 404

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Usuário deletado com sucesso"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------
# MAIN
# ------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
