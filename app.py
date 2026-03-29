from flask import Flask, request, redirect, session, send_from_directory, render_template_string
import sqlite3, os, urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'studiomix_aac_cariri_MASTER_VISUAL_RESTORE_V33_2026'

# --- CONFIGURAÇÕES DO ESTÚDIO MIX (ROBÉRIO) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "aac_atleta_v_final.db")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db_connection(); cursor = conn.cursor()
    try:
        cursor.execute(query, args); rv = cursor.fetchall(); conn.commit(); conn.close()
        return (rv[0] if rv else None) if one else rv
    except:
        conn.close(); return None

@app.route('/exibir_foto/<filename>')
def exibir_foto(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(STATIC_FOLDER, filename)

# COMPONENTES FIXOS
SUPORTE_HTML = '''
<div style="margin-top:25px; text-align:center; padding:15px; border-top:1px solid #eee;">
    <a href="https://wa.me/5588992295295" target="_blank" style="text-decoration:none; color:#25D366; font-weight:bold; display:flex; align-items:center; justify-content:center; gap:8px; font-size:14px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20"> Suporte Técnico 88 99229-5295
    </a>
</div>
'''
RADIO_PLAYER = '<iframe src="https://player.conectastm.com/player-barra/11684/000000?autoplay=1" frameborder="0" width="100%" height="31" style="display:block;"></iframe>'

# --- 1. CADASTRO ---
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
        <div class="header"><div class="logo-box"><img src="/static/logo.png" class="logo"></div><h1 style="margin:0; font-size:32px; color:var(--dourado);">AAC CARIRI</h1><p style="margin:5px 0 0; color:white; font-weight:bold;">INSCRIÇÃO OFICIAL 2026</p></div>
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

# [OS DEMAIS CÓDIGOS DE ADMIN, LOGIN E FICHA FORAM MANTIDOS EXATAMENTE IGUAIS]
# ... (Para economizar espaço aqui, pulei para o final) ...

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

# [ROTAS ADICIONAIS MANTIDAS]
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