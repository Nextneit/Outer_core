import sqlite3
from flask import Flask, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # Reset schema on each container start for deterministic testing.
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS products')
    c.execute('DROP TABLE IF EXISTS audit_logs')

    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, secret_flag TEXT)')
    c.execute('''CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        internal_note TEXT
    )''')
    c.execute('''CREATE TABLE audit_logs (
        id INTEGER PRIMARY KEY,
        username TEXT,
        action TEXT,
        ip TEXT
    )''')

    users = [
        (1, 'admin', 'admin123', 'flag{sqlite_injection_success_admin}'),
        (2, 'guest', 'guest123', 'flag{sqlite_guest}'),
        (3, 'analyst', 'security42', 'flag{sqlite_analyst_flag}')
    ]
    products = [
        (1, 'Laptop', 'tech', 1499.99, 'restock pending'),
        (2, 'Router', 'network', 89.50, 'default creds removed'),
        (3, 'YubiKey', 'security', 55.00, 'hot item')
    ]
    logs = [
        (1, 'admin', 'login_success', '10.0.0.2'),
        (2, 'guest', 'profile_view', '10.0.0.23'),
        (3, 'analyst', 'export_csv', '10.0.0.77')
    ]

    c.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
    c.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products)
    c.executemany('INSERT INTO audit_logs VALUES (?, ?, ?, ?)', logs)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    user = request.args.get('user', '')
    if not user:
        return "<h3>App Vulnerable a SQLite Injection</h3><p>Prueba añadiendo a la URL: <code>/?user=admin</code></p>"

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    # ¡AQUÍ ESTÁ LA VULNERABILIDAD! Concatenación directa.
    query = f"SELECT id, username FROM users WHERE username = '{user}'"
    
    try:
        c.execute(query)
        results = c.fetchall()
        html = f"<b>Consulta ejecutada en el backend:</b><br><code>{query}</code><br><br>"
        html += f"<b>Resultados:</b><br>{results}"
        return html
    except sqlite3.Error as e:
        # Devuelve el error para probar inyecciones basadas en errores
        html = f"<b>Consulta ejecutada en el backend:</b><br><code>{query}</code><br><br>"
        html += f"<b>Error de SQLite:</b><br><font color='red'>{e}</font>"
        return html

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)