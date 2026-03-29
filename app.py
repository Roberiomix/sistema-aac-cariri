from flask import Flask, request, redirect, session, render_template_string
import psycopg2, psycopg2.extras
import os
import urllib.parse

app = Flask(__name__)
app.secret_key = 'studiomix_aac_cariri_2026'

# --- CONFIGURAÇÃO BLINDADA DO BANCO ---
password = urllib.parse.quote_plus('roberiomix2026')
DATABASE_URL = f"postgresql://postgres.bshyfeshtojiucusqzri:{password}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, connect_timeout=10)
    except:
        return None

@app.route('/')
def index():
    # Tela de aviso profissional que você solicitou
    return render_template_string('''
        <body style="background:#004a23; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; color:white; text-align:center; margin:0;">
            <img src="https://sistema-aac-cariri.onrender.com/static/logo.aac.png" height="100" style="margin-bottom:20px;" onerror="this.style.display='none'">
            <div style="background:rgba(255,255,255,0.1); padding:40px; border-radius:20px; border:2px solid #ceb05c; max-width:85%; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <h2 style="color:#ceb05c; margin-top:0;">Portal do Atleta AAC</h2>
                <p style="font-size:1.3rem; line-height:1.6;">Por favor, aguarde um instante.<br>Estamos carregando o sistema de cadastro do portal do atleta.</p>
                <div class="loader"></div>
            </div>
            <script>setTimeout(function(){ window.location.href = "/login"; }, 6000);</script>
            <style>
                .loader { border: 5px solid #f3f3f3; border-top: 5px solid #ceb05c; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 30px auto; }
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        </body>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('u') == 'admin' and request.form.get('p') == 'mix2026':
            session['adm'] = True
            return redirect('/admin_studiomix')
    return render_template_string('''
        <body style="background:#004a23; display:flex; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; margin:0;">
            <form method="POST" style="background:white; padding:40px; border-radius:20px; text-align:center; width:320px; box-shadow:0 10px 25px rgba(0,0,0,0.5);">
                <h2 style="color:#004a23; margin-bottom:30px;">Acesso AAC</h2>
                <input name="u" placeholder="Usuário" required style="width:100%; padding:12px; margin-bottom:15px; border:1px solid #ddd; border-radius:8px;">
                <input type="password" name="p" placeholder="Senha" required style="width:100%; padding:12px; margin-bottom:25px; border:1px solid #ddd; border-radius:8px;">
                <button type="submit" style="background:#004a23; color:#ceb05c; padding:15px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:1rem;">ENTRAR NO PORTAL</button>
            </form>
        </body>
    ''')

@app.route('/admin_studiomix')
def admin():
    if not session.get('adm'): return redirect('/login')
    conn = get_db_connection()
    if not conn: return "Erro de Conexão: Verifique se a senha no Supabase é 'roberiomix2026'."
    
    atletas = []
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM moradores ORDER BY nome ASC")
        atletas = cur.fetchall()
        conn.close()
    except:
        conn.close()
        return "Erro ao ler tabela. Certifique-se de que criou a tabela 'moradores' no SQL Editor do Supabase."

    return render_template_string('''
        <body style="background:#f4f4f4; font-family:sans-serif; margin:0;">
            <div style="background:#004a23; color:white; padding:20px; display:flex; justify-content:space-between; align-items:center;">
                <h2 style="margin:0;">AAC - Painel Administrativo</h2>
                <a href="/login" style="color:#ceb05c; font-weight:bold; text-decoration:none;">SAIR</a>
            </div>
            <div style="padding:20px;">
                <div style="background:white; border-radius:10px; padding:20px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                    <table style="width:100%; border-collapse:collapse;">
                        <tr style="background:#ceb05c; color:#004a23;">
                            <th style="padding:12px; text-align:left;">Atleta</th>
                            <th style="padding:12px; text-align:left;">CPF</th>
                            <th style="padding:12px; text-align:left;">WhatsApp</th>
                        </tr>
                        {% for a in atletas %}
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:12px;">{{ a.nome }}</td>
                            <td style="padding:12px;">{{ a.cpf }}</td>
                            <td style="padding:12px;">{{ a.whatsapp }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    {% if not atletas %}<p style="text-align:center; padding:30px; color:#666;">Sistema Conectado! Nenhum atleta cadastrado ainda.</p>{% endif %}
                </div>
            </div>
        </body>
    ''', atletas=atletas)

if __name__ == "__main__":
    app.run(debug=False)
