from flask import Flask, request, redirect, session, render_template_string
import psycopg2, psycopg2.extras
import urllib.parse
from datetime import timedelta

app = Flask(__name__)
# Chave mestra reforçada
app.secret_key = 'studiomix_aac_2026_oficial'
app.config['SESSION_COOKIE_NAME'] = 'aac_session_admin'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)

# --- BANCO DE DADOS ---
senha_banco = 'roberiomix2026'
senha_limpa = urllib.parse.quote_plus(senha_banco)
DATABASE_URL = f"postgresql://postgres.bshyfeshtojiucusqzri:{senha_limpa}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, connect_timeout=10)
    except:
        return None

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        # O .strip() garante que não vá nenhum espaço em branco
        u = str(request.form.get('u')).strip()
        p = str(request.form.get('p')).strip()
        
        # ACEITA OS DOIS LOGINS POR SEGURANÇA
        if (u == 'roberiomix2026' and p == 'roberiomix2026') or (u == 'admin' and p == 'mix2026'):
            session.clear() # Limpa qualquer lixo de sessão anterior
            session['adm_logado'] = True
            return redirect('/admin_studiomix')
        else:
            msg = "Usuário ou Senha não conferem!"
            
    return render_template_string('''
        <body style="background:#004a23; display:flex; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; margin:0;">
            <form method="POST" style="background:white; padding:40px; border-radius:20px; text-align:center; width:300px; box-shadow:0 10px 25px rgba(0,0,0,0.5);">
                <h2 style="color:#004a23; margin-bottom:20px;">AAC - Portal</h2>
                {% if msg %}<p style="color:red; background:#fee; padding:10px; border-radius:5px; font-size:13px; font-weight:bold;">{{ msg }}</p>{% endif %}
                <input name="u" placeholder="Usuário" required style="width:100%; padding:12px; margin-bottom:15px; border:1px solid #ddd; border-radius:8px;">
                <input type="password" name="p" placeholder="Senha" required style="width:100%; padding:12px; margin-bottom:25px; border:1px solid #ddd; border-radius:8px;">
                <button type="submit" style="background:#004a23; color:#ceb05c; padding:15px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:16px;">ENTRAR AGORA</button>
            </form>
        </body>
    ''', msg=msg)

@app.route('/admin_studiomix')
def admin():
    # Se o crachá não estiver na mão, volta pro login
    if not session.get('adm_logado'):
        return redirect('/login')
        
    conn = get_db_connection()
    if not conn: 
        return "Erro de conexão com o banco. Aguarde 30 segundos e atualize a página."
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM moradores ORDER BY nome ASC")
    atletas = cur.fetchall()
    conn.close()
    
    return render_template_string('''
        <body style="background:#f4f4f4; font-family:sans-serif; margin:0;">
            <div style="background:#004a23; color:white; padding:20px; display:flex; justify-content:space-between; align-items:center;">
                <h2 style="margin:0;">AAC - Painel Administrativo</h2>
                <a href="/login" style="color:#ceb05c; font-weight:bold; text-decoration:none; border:1px solid #ceb05c; padding:5px 10px; border-radius:5px;">SAIR</a>
            </div>
            <div style="padding:20px;">
                <div style="background:white; border-radius:10px; padding:20px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                    <table style="width:100%; border-collapse:collapse;">
                        <tr style="background:#ceb05c; color:#004a23;">
                            <th style="padding:12px; text-align:left;">Atleta</th>
                            <th style="padding:12px; text-align:left;">WhatsApp</th>
                        </tr>
                        {% for a in atletas %}
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:12px;">{{ a.nome }}</td>
                            <td style="padding:12px;">{{ a.whatsapp }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    {% if not atletas %}<p style="text-align:center; padding:30px; color:#666;">Sistema Conectado com Sucesso! Aguardando o primeiro cadastro.</p>{% endif %}
                </div>
            </div>
        </body>
    ''', atletas=atletas)

if __name__ == "__main__":
    app.run(debug=False)
