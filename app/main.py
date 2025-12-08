from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Variáveis de ambiente corretas de acordo com o docker-compose
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")  # deve bater com .env / compose

def get_connection():
    """Abre conexão com o Postgres. Se desejar, pode adicionar retry/timeout aqui."""
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# ------------------------
# Funções de acesso ao banco (separadas para facilitar mock nos testes)
# ------------------------
def fetch_users():
    """Retorna lista de usuários como dicionários."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users;")
        rows = cur.fetchall()
        cur.close()
        # converter tuplas para dicts
        return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    finally:
        if conn:
            conn.close()

def insert_user(name: str, email: str):
    """Insere usuário e retorna o id inserido."""
    conn = None
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
        return user_id
    finally:
        if conn:
            conn.close()

# ------------------------
# ROTA RAIZ
# ------------------------
@app.route('/')
def home():
    return jsonify({"message": "API funcionando!"})

# ------------------------
# CRUD DE USUÁRIOS (uses helper functions)
# ------------------------
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = fetch_users()
        return jsonify(users), 200
    except Exception as e:
        # Log real em produção; aqui retornamos erro para facilitar debugging
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Nome e email são obrigatórios"}), 400

    try:
        user_id = insert_user(name, email)
        return jsonify({"id": user_id, "name": name, "email": email}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json or {}
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
            cur.close()
            conn.close()
            return jsonify({"error": "Usuário não encontrado"}), 404
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Usuário atualizado com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
        if cur.rowcount == 0:
            cur.close()
            conn.close()
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
