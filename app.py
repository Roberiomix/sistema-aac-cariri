from flask import Flask, request, redirect, session, send_from_directory, render_template_string
import sqlite3, os, urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'studiomix_aac_cariri_MASTER_VISUAL_RESTORE_V33_2026'

# --- CONFIGURAÇÕES ADAPTADAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "aac_atleta_v_final.db")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db_connection(); cursor = conn.cursor()
    try:
        cursor.execute(query, args); rv = cursor.fetchall(); conn.commit(); conn.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        print(f"Erro no Banco: {e}")
        conn.close(); return None

@app.route('/exibir_foto/<filename>')
def exibir_foto(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(STATIC_FOLDER, filename)

SUPORTE_HTML = '''
<div style="margin-top:25px; text-align:center; padding:15px; border-top:1px solid #eee;">
    <a href="https://wa.me/5588992295295" target="_blank" style="text-decoration:none; color:#25D366; font-weight:bold; display:flex; align-items:center; justify-content:center; gap:8px; font-size:14px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20"> Suporte Técnico 88 99229-5295
    </a>
</div>
'''
RADIO_PLAYER = '<iframe src="https://player.conectastm.com/player-barra/11684/000000?autoplay=1" frameborder="0" width="100%" height="31" style="display:block;"></iframe>'

@app.route("/")
def index():
    return render_template_string('''
    <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Inscrição Oficial AAC Cariri</title>
    <style>
        :root { --verde: #004a23; --dourado: #ceb05c; --bg: #f0f2f5; }
        body{font-family:'Segoe UI', sans-serif; background: var(--bg); margin:0; padding:0;}
        .card{background:white; max-width:600px; margin:20px auto; border-radius:25px; box-shadow:0 15px 35px rgba(0,0,0,0.1); overflow:hidden;}
        .header{background: var(--verde); padding:40px; text-align:center;}
        .logo-box{background:white; width:120px; height:120px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; box-shadow:0 8px 20px rgba(0,0,0,0.2);}
        .logo{height:90px;}
        .form-content{padding:30px;}
        .btn-ja-cadastrado{background: var(--dourado); color: var(--verde); padding:15px; border-radius:12px; text-decoration:none; display:block; font-weight:bold; margin-bottom:25px; border:2px solid var(--verde); text-align:center;}
        .section-title{background:#e8f5e9; color:var(--verde); padding:15px; border-radius:12px; margin:30px 0 10px; font-weight:800; text-transform:uppercase; font-size:13px; border-left:6px solid var(--dourado);}
        .help-text{font-size:12px; color:#c2410c; background:#fff3e0; padding:12px; border-radius:8px; border-left:4px solid #f97316; margin-bottom:15px; font-weight:bold;}
        input, select{width:100%; padding:15px; margin:10px 0; border-radius:12px; border:1px solid #ddd; font-size:16px; box-sizing:border-box;}
        .btn-submit{width:100%; padding:22px; background:var(--verde); color:var(--dourado); border-radius:15px; border:none; font-weight:900; font-size:20px; cursor:pointer; margin-top:30px; text-transform:uppercase;}
    </style></head><body>
    <div class="card">
        <div class="header">
            <div class="logo-box">
                <img src="/static/logo.aac.jpeg" class="logo">
            </div>
            <h1 style="margin:0; font-size:32px; color:var(--dourado);">AAC CARIRI</h1>
            <p style="margin:5px 0 0; color:white; font-weight:bold;">INSCRIÇÃO OFICIAL 2026</p>
        </div>
        <div class="form-content">
            <a href="/login_atleta" class="btn-ja-cadastrado">⚽ JÁ TENHO CADASTRO? CLIQUE AQUI</a>
            <form action="/cadastrar" method="POST" enctype="multipart/form-data">
                <div class="section-title">👤 1. DADOS DO ATLETA</div>
                <input name="nome" placeholder="Nome Completo" required><input name="nasc" type="date" required><input name="nat" placeholder="Naturalidade">
                <input name="rg" placeholder="RG"><input name="cpf" placeholder="CPF" required><input name="nis" placeholder="Número do NIS">
                <div class="section-title">⚽ 2. FICHA TÉCNICA E SAÚDE</div>
                <input name="posicao" placeholder="Posição (Ex: Atacante, Goleiro)"><input name="pe" placeholder="Pé Dominante"><input name="sangue" placeholder="Tipo Sanguíneo">
                <input name="peso" placeholder="Peso (kg)"><input name="altura" placeholder="Altura"><input name="clube" placeholder="Clube" value="AAC CARIRI">
                <div class="section-title">👨‍👩‍👦 3. FAMÍLIA E RESPONSÁVEIS</div>
                <input name="mae" placeholder="Mãe"><input name="mae_cpf" placeholder="CPF Mãe"><input name="pai" placeholder="Pai"><input name="pai_cpf" placeholder="CPF Pai"><input name="resp_atleta" placeholder="Responsável Legal" required>
                <div class="section-title">🏫 4. ESTUDOS</div>
                <input name="escola" placeholder="Escola"><input name="serie" placeholder="Série/Ano"><input name="turma" placeholder="Turma"><input name="turno" placeholder="Turno">
                <div class="section-title">📍 5. LOCALIZAÇÃO</div>
                <input name="whatsapp" placeholder="WhatsApp" required><input name="tel_resp" placeholder="Tel Emergência"><input name="email" type="email" placeholder="E-mail">
                <input name="endereco" placeholder="Endereço"><input name="bairro" placeholder="Bairro"><input name="cidade" placeholder="Cidade" value="Barbalha"><input name="cep" placeholder="CEP">
                <div class="section-title">🔑 6. ACESSO</div>
                <div class="help-text">👉 ORIENTAÇÃO: CRIE UM USUÁRIO E SENHA ABAIXO.</div>
                <input name="user" placeholder="Usuário" required><input type="password" name="pass" placeholder="Senha" required>
                <div class="section-title">📸 7. FOTO OFICIAL</div>
                <div class="help-text">📷 ORIENTAÇÃO: ENVIE UMA FOTO DO ROSTO COM FUNDO LIMPO (3X4).</div>
                <input type="file" name="foto" accept="image/*" required style="padding:10px; background:white; border: 2px dashed var(--verde); border-radius:12px; width:100%;">
                <button type="submit" class="btn-submit">FINALIZAR INSCRIÇÃO</button>
            </form>
            {{ suporte | safe }}
        </div></div></body></html>
    ''', suporte=SUPORTE_HTML)

# MANTIVE O RESTANTE DO CÓDIGO (ADMIN, LOGIN, MEU PORTAL) EXATAMENTE IGUAL
# APENAS AJUSTANDO OS CAMINHOS DAS IMAGENS ONDE APARECEM

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('u')=='admin' and request.form.get('p')=='mix2026': session['adm']='admin'; return redirect('/admin_studiomix')
    return render_template_string('''<body style="background:#004a23; display:flex; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; margin:0;"><form method="POST" style="background:white; padding:40px; border-radius:25px; text-align:center; border:4px solid #ceb05c; width:340px;"><img src="/static/logo.aac.jpeg" height="55"><h2>Painel Gestor</h2><input name="u" placeholder="Usuário" style="width:100%; padding:12px; margin-bottom:10px; border-radius:10px; border:1px solid #ddd; box-sizing:border-box;"><input type="password" name="p" placeholder="Senha" style="width:100%; padding:12px; margin-bottom:20px; border-radius:10px; border:1px solid #ddd; box-sizing:border-box;"><button style="background:#004a23; color:#ceb05c; width:100%; padding:18px; border-radius:12px; border:none; font-weight:bold; cursor:pointer;">ENTRAR NO PAINEL</button>{{ suporte | safe }}</form></body>''', suporte=SUPORTE_HTML)

@app.route("/login_atleta", methods=['GET', 'POST'])
def login_atleta():
    if request.method == 'POST':
        u = request.form.get('u'); p = request.form.get('p')
        atleta = query_db("SELECT id FROM moradores WHERE login_usuario=? AND senha=?", (u, p), one=True)
        if atleta: session['atleta_id'] = atleta['id']; return redirect('/meu_portal')
    return render_template_string('''<body style="background:#004a23; display:flex; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; margin:0;"><form method="POST" action="/login_atleta" style="background:white; padding:40px; border-radius:25px; text-align:center; border:4px solid #ceb05c; width:340px;"><img src="/static/logo.aac.jpeg" height="55"><h2>Portal do Atleta</h2><input name="u" placeholder="Usuário" required style="width:100%; padding:15px; margin-bottom:10px; border-radius:10px; border:1px solid #ddd; box-sizing:border-box;"><input type="password" name="p" placeholder="Senha" required style="width:100%; padding:15px; margin-bottom:20px; border-radius:10px; border:1px solid #ddd; box-sizing:border-box;"><button type="submit" style="background:#004a23; color:#ceb05c; padding:18px; width:100%; border-radius:12px; border:none; font-weight:900; cursor:pointer;">ENTRAR</button>{{ suporte | safe }}</form></body>''', suporte=SUPORTE_HTML)

@app.route("/meu_portal")
def meu_portal():
    if not session.get('atleta_id'): return redirect('/login_atleta')
    a = query_db("SELECT * FROM moradores WHERE id=?", (session['atleta_id'],), one=True)
    if not a: return redirect('/logout')
    if a['liberada'] != 'Sim':
        return render_template_string('<body style="background:#004a23; color:white; text-align:center; padding-top:100px; font-family:sans-serif;"><h1>Aguardando Liberação...</h1><p>Sua carteirinha será liberada em breve.</p><a href="/logout" style="color:#ceb05c;">Sair</a><br><br>{{ radio | safe }}{{ suporte | safe }}</body>', radio=RADIO_PLAYER, suporte=SUPORTE_HTML)
    
    try: data_br = datetime.strptime(a['nascimento'], '%Y-%m-%d').strftime('%d/%m/%Y')
    except: data_br = a['nascimento']
    
    return render_template_string('''<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>@media all {:root { --verde: #004a23; --dourado: #ceb05c; }body{ background:#f0f2f5; font-family:sans-serif; padding:0; text-align:center; margin:0;}.credit-card { width:350px; height:215px; border-radius:18px; position:relative; color:white; background: linear-gradient(135deg, #004a23 0%, #002d15 100%) !important; border:2px solid var(--dourado); overflow:hidden; -webkit-print-color-adjust: exact; margin:20px auto; box-shadow:0 15px 35px rgba(0,0,0,0.3); }.front .photo-box { position:absolute; top:15px; left:15px; width:110px; height:140px; border-radius:10px; border:2px solid var(--dourado); background:white; overflow:hidden; z-index:1;}.front .logo-mini { position:absolute; top:12px; right:12px; height:45px; background:white; border-radius:50%; padding:5px; z-index:10; }.front .posicao-central { position:absolute; top:80px; left:135px; right:10px; text-align:center; font-weight:900; color:var(--dourado); font-size:16px; text-transform:uppercase; z-index:5; }.front .atleta-info { position:absolute; bottom:12px; left:135px; right:15px; text-align:center; z-index:10; }.back .details { padding:15px; text-align:left; font-size:10px; line-height:1.3; margin-top:10px; }.back .pix-box { position:absolute; bottom:10px; right:10px; width:75px; height:75px; background:white; padding:4px; border-radius:8px; text-align:center;}.back .pix-text { position:absolute; bottom:92px; right:10px; font-size:6px; font-weight:bold; color:var(--dourado); text-transform:uppercase; width:75px; text-align:center; }}@media print { .btn-print, h2, .sop, .radio-box { display:none; } }</style></head><body><div class="radio-box" style="position:sticky; top:0; z-index:1000;">{{ radio | safe }}</div><div class="card-container" style="padding-top:20px;"><div class="credit-card front"><img src="/static/logo.aac.jpeg" class="logo-mini"><div class="posicao-central">{{a['posicao']}}</div><div class="photo-box"><img src="/exibir_foto/{{a['foto']}}" style="width:100%; height:100%; object-fit:cover;"></div><div class="atleta-info"><div style="font-size:15px; font-weight:900; color:white; text-transform:uppercase;">{{a['nome']}}</div><div style="font-size:10px; color:var(--dourado); letter-spacing:1px; font-weight:bold; margin-top:3px;">ATLETA OFICIAL AAC</div></div></div><div class="credit-card back"><div style="width:100%; height:40px; background:#111; margin-top:20px;"></div><div class="details"><b>MÃE:</b> {{a['mae']}}<br><b>PAI:</b> {{a['pai']}}<br><b>CONTATO:</b> {{a['whatsapp']}}<br><b>NASCIMENTO:</b> {{data_br}}<br><b>CPF:</b> {{a['cpf']}}<br><br><b style="color:var(--dourado);">ASSOCIAÇÃO ATLÉTICA CARIRI</b></div><div class="pix-text">SCANEE PARA PAGAR SUA MENSALIDADE</div><div class="pix-box"><img src="/static/qrcod.jpg" style="width:100%;"></div></div></div><button onclick="window.print()" class="btn-print" style="padding:15px 30px; background:var(--verde); color:var(--dourado); border:none; border-radius:15px; font-weight:bold; cursor:pointer; margin-bottom:20px;">🖨️ IMPRIMIR CARTEIRINHA</button><div class="sop">{{ suporte | safe }}</div></body></html>''', a=a, data_br=data_br, suporte=SUPORTE_HTML, radio=RADIO_PLAYER)

# MANTENHA AS DEMAIS FUNÇÕES (CADASTRAR, ADMIN, ETC)
@app.route("/admin_studiomix")
def admin():
    if not session.get('adm'): return redirect('/login')
    m_list = query_db("SELECT * FROM moradores ORDER BY id DESC")
    links = {}
    if m_list:
        for m in m_list:
            msg = f"Olá {m['nome']}! Cadastro APROVADO na AAC Cariri. Link: {request.url_root}login_atleta"
            links[m['id']] = f"https://wa.me/55{m['whatsapp'].replace('(','').replace(')','').replace(' ','').replace('-','')}?text={urllib.parse.quote(msg)}"
    return render_template_string('''<body style="font-family:sans-serif; background:#f4f7f6; padding:0; margin:0;"><div style="position:sticky; top:0; z-index:1000;">{{ radio | safe }}</div><div style="max-width:1150px; margin:20px auto; background:white; border-radius:30px; overflow:hidden;"><div style="background:#004a23; padding:35px; display:flex; justify-content:space-between; align-items:center;"><h1 style="color:#ceb05c; margin:0;">Gestão AAC</h1><a href="/logout" style="background:#ff4757; color:white; padding:10px 20px; border-radius:12px; text-decoration:none; font-weight:bold;">SAIR</a></div><div style="padding:30px;">{% for m in m_list %}<div style="background:#fff; border:1px solid #eee; margin-bottom:15px; padding:20px; border-radius:20px; display:flex; justify-content:space-between; align-items:center;"><div style="flex:1;"><div style="font-weight:bold; font-size:18px; color:#004a23; text-transform:uppercase;">{{m['nome']}}</div><div style="font-size:13px; color:#555; margin-top:5px;">👤 <b>USUÁRIO:</b> {{m['login_usuario']}} | 🔑 <b>SENHA:</b> {{m['senha']}}<br>💰 <b>MENSALIDADES:</b> {{m['mensalidades_pagas'] or '0'}}</div></div><div style="display:flex; gap:10px;"><a href="/ver_ficha/{{m['id']}}" style="background:#004a23; color:white; padding:10px 15px; border-radius:10px; text-decoration:none; font-size:12px; font-weight:bold;">FICHA</a><a href="{{links[m['id']]}}" target="_blank" style="background:#25D366; color:white; padding:10px 15px; border-radius:10px; text-decoration:none; font-size:12px; font-weight:bold;">📲 ZAP</a><a href="/toggle_status/{{m['id']}}" style="padding:10px 15px; border-radius:10px; text-decoration:none; font-size:12px; font-weight:bold; background:{% if m['liberada']=='Sim' %}#16a34a{% else %}#ceb05c{% endif %}; color:white;">{% if m['liberada']=='Sim' %}✅ OK{% else %}🔓 LIBERAR{% endif %}</a><a href="/del_atleta/{{m['id']}}" onclick="return confirm('Excluir?')" style="color:#ccc; font-size:20px; text-decoration:none;">&times;</a></div></div>{% endfor %}</div>{{ suporte | safe }}</div></body>''', m_list=m_list, links=links, suporte=SUPORTE_HTML, radio=RADIO_PLAYER)

@app.route("/ver_ficha/<int:id>")
def ver_ficha(id):
    if not session.get('adm'): return redirect('/login')
    a = query_db("SELECT * FROM moradores WHERE id=?", (id,), one=True)
    return render_template_string('''<body style="font-family:serif; padding:20px; background:white; line-height:1.5;"><div style="border:5px double #004a23; padding:40px; max-width:850px; margin:auto; position:relative;"><div style="position:absolute; right:40px; top:120px; border:4px solid #004a23; padding:5px;"><img src="/exibir_foto/{{a['foto']}}" style="width:145px; height:185px; object-fit:cover;"></div><center><img src="/static/logo.aac.jpeg" height="90"><h1 style="color:#004a23; margin:10px 0; padding-right:150px;">FICHA DE INSCRIÇÃO</h1></center><br><hr style="border:2px solid #004a23;"><div style="font-size:14px; margin-top:20px;"><p><b>ATLETA:</b> {{a['nome']}} | <b>CPF:</b> {{a['cpf']}}<br><b>POSIÇÃO:</b> {{a['posicao']}} | <b>NASC:</b> {{a['nascimento']}}</p></div><center><button onclick="window.print()">IMPRIMIR</button></center></div></body>''', a=a)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    try:
        f = request.form; file = request.files.get("foto")
        fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        file.save(os.path.join(UPLOAD_FOLDER, fname))
        query_db("""INSERT INTO moradores (nome, cpf, nascimento, rg, naturalidade, posicao, pe, peso, altura, clube_origem, mae, mae_cpf, pai, pai_cpf, nis, escola, serie, turma, turno, whatsapp, tel_responsavel, endereco, bairro, cidade, cep, resp_atleta, login_usuario, senha, email, foto, tipo_sanguineo, liberada)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                 (f.get('nome').upper(), f.get('cpf'), f.get('nasc'), f.get('rg'), f.get('nat'), f.get('posicao'), f.get('pe'), f.get('peso'), f.get('altura'), f.get('clube'), f.get('mae'), f.get('mae_cpf'), f.get('pai'), f.get('pai_cpf'), f.get('nis'), f.get('escola'), f.get('serie'), f.get('turma'), f.get('turno'), f.get('whatsapp'), f.get('tel_resp'), f.get('endereco'), f.get('bairro'), f.get('cidade'), f.get('cep'), f.get('resp_atleta'), f.get('user'), f.get('pass'), f.get('email'), fname, f.get('sangue'), 'Não'))
        return redirect('/sucesso')
    except Exception as e: return str(e)

@app.route("/toggle_status/<int:id>")
def toggle_status(id):
    if not session.get('adm'): return redirect('/login')
    atleta = query_db("SELECT liberada FROM moradores WHERE id=?", (id,), one=True)
    novo = 'Não' if atleta['liberada'] == 'Sim' else 'Sim'
    query_db("UPDATE moradores SET liberada=? WHERE id=?", (novo, id))
    return redirect('/admin_studiomix')

@app.route("/logout")
def logout(): session.clear(); return redirect('/')

@app.route("/del_atleta/<int:id>")
def del_atleta(id):
    query_db("DELETE FROM moradores WHERE id=?", (id,)); return redirect('/admin_studiomix')

@app.route("/sucesso")
def sucesso():
    return render_template_string('<body style="background:#004a23; height:100vh; display:flex; align-items:center; justify-content:center; font-family:sans-serif; text-align:center;"><div style="background:white; padding:50px; border-radius:30px; border:5px solid #ceb05c;"><h1>✅ SUCESSO!</h1><p>Inscrição enviada.</p><a href="/login_atleta" style="background:#004a23; color:#ceb05c; padding:15px; border-radius:15px; text-decoration:none; font-weight:bold; display:block;">ENTRAR NO PORTAL</a></div></body>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
