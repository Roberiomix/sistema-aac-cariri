from flask import Flask, request, redirect, session, render_template_string
import psycopg2, psycopg2.extras
import os

app = Flask(__name__)
app.secret_key = 'studiomix_aac_cariri_2026'

# --- ABAIXO: COLOQUE SUA SENHA NO LUGAR DE 'SUA_SENHA_AQUI' ---
DATABASE_URL = "postgresql://postgres.bshyfeshtojiucusqzri:roberiomix2026@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('u')
        p = request.form.get('p')
        if u == 'admin' and p == 'mix2026':
            session['adm'] = True
            return redirect('/admin_studiomix')
    return render_template_string('''
        <body style="background:#004a23; display:flex; align-items:center; justify-content:center; height:100vh; font-family:sans-serif;">
            <form method="POST" style="background:white; padding:40px; border-radius:20px; text-align:center;">
                <img src="https://sistema-aac-cariri.onrender.com/static/logo.aac.png" height="60"><br><br>
                <input name="u" placeholder="Usuário" style="width:100%; padding:10px; margin-bottom:10px;"><br>
                <input type="password" name="p" placeholder="Senha" style="width:100%; padding:10px; margin-bottom:20px;"><br>
                <button type="submit" style="background:#004a23; color:#ceb05c; padding:10px 20px; border:none; cursor:pointer; font-weight:bold;">ENTRAR</button>
            </form>
        </body>
    ''')

@app.route('/admin_studiomix')
def admin():
    if not session.get('adm'): return redirect('/login')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM moradores ORDER BY nome ASC")
    atletas = cur.fetchall()
    conn.close()
    
    return render_template_string('''
        <body style="background:#f0f0f0; font-family:sans-serif; margin:0;">
            <div style="background:#004a23; color:white; padding:20px; display:flex; justify-content:space-between;">
                <h2>Gestão AAC - Atletas</h2>
                <a href="/login" style="color:white; text-decoration:none;">SAIR</a>
            </div>
            <div style="padding:20px;">
                <table border="1" style="width:100%; background:white; border-collapse:collapse;">
                    <tr style="background:#ceb05c;"><th>Nome</th><th>CPF</th><th>WhatsApp</th></tr>
                    {% for a in atletas %}
                    <tr><td>{{ a.nome }}</td><td>{{ a.cpf }}</td><td>{{ a.whatsapp }}</td></tr>
                    {% endfor %}
                </table>
                {% if not atletas %}<p>Nenhum atleta cadastrado no Supabase ainda.</p>{% endif %}
            </div>
        </body>
    ''', atletas=atletas)

if __name__ == "__main__":
    app.run(debug=True)
