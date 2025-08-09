import os, uuid
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
email = os.getenv('EMAIL_USUARIO')
senha = os.getenv('SENHA_USUARIO')

 #será que o fato disso estar fora da função vai dar problema?
def gerar_client():
    return create_client(url, key)

def gerar_codigo_unico(client):
    """Cria um código único de validação para o certificado"""
    while True:
        codigo = uuid.uuid4().hex[:12]
        res = client.table("certificados").select("codigo_validacao").eq("codigo_validacao", codigo).execute()
        if len(res.data) == 0:
            return codigo  # não existe no banco, pode usar

def autenticar_supabase(client):
    """Função que autentica no supabase""" # PRECISO MELHORAR
    auth_response = client.auth.sign_in_with_password({
        "email": email,
        "password": senha
    })

    token = auth_response.session.access_token
    refresh_token = auth_response.session.refresh_token
    client.auth.set_session(token, refresh_token)

def registra_novo_usuario_certificado(client, nome, email, id_membro):
    """Cria um novo usuário no banco de dados e retorna o ID do usuário criado."""
    res = client.table("usuarios_certificados").insert({
        "nome": nome,
        "email": email,
        "id_membro": id_membro
    }).execute()

    # Pega o ID retornado (assumindo que a tabela retorna o registro criado)
    id_usuario = res.data[0]['id']
    return id_usuario

def registrar_certificado(client, nome, curso, carga_horaria, data_emissao, data_certificacao, id_usuario):
    """Cria um novo certificado vinculado a um usuário e retorna o código de validação."""
    codigo = gerar_codigo_unico(client)

    client.table("certificados").insert({
        "codigo_validacao": codigo,
        "nome": nome,
        "curso": curso,
        "carga_horaria": carga_horaria,
        "data_certificacao": data_certificacao,
        "usuario_certificado_id": id_usuario
    }).execute()

    return codigo

def subir_pdf_para_supabase(client,caminho_pdf, caminho_storage):
    """Envia um arquivo PDF para o Supabase."""
    client.storage.from_("certificados").upload(
        path=caminho_storage,
        file=caminho_pdf,
        file_options={"content-type": "application/pdf"}
    )
    url_publica = client.storage.from_("certificados").get_public_url(caminho_storage)
    return url_publica

def atualizar_url_certificado(client, codigo_validacao, url_arquivo):
    """Atualiza a URL do arquivo PDF na linha do certificado correspondente ao código."""
    client.table("certificados").update({
        "arquivo_url": url_arquivo
    }).eq("codigo_validacao", codigo_validacao).execute()
