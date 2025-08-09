from fastapi import FastAPI, Request
from funcoes_certificado import *
from funcoes_supabase import *
from funcoes_email import *
from funcoes_circle import *

app = FastAPI()

from datetime import date

@app.post("/webhook")
async def receber_webhook(request: Request):
    """Webhook para disparo automático de e-mails"""
    payload = await request.json()

    client = gerar_client()
    autenticar_supabase(client)

    # Trata o dado recebido do webhook e retorna o nome completo do usuário
    id = recebe_webhook_e_captura_nome(payload)
    data = dados_do_usuario_circle(id)

    # Organiza os dados necessários para o preenchimento do certificado
    nome = data.get("name", "")
    email = data.get("email", "")
    curso="Certificação: Financeiro no Superlógica Imobi - Módulo Fundamental"
    carga_horaria="24"

    # Registra um novo usuário certificado
    id_usuario = registra_novo_usuario_certificado(client, nome, email, id)

    hoje = date.today()
    data_emissao = hoje.strftime("%d de %B de %Y")
    data_certificacao = hoje.strftime("%d/%m/%Y")

    # Registra um novo certificado no banco e armazena o código único
    codigo = registrar_certificado(client, nome, curso, carga_horaria, data_emissao, data_certificacao, id_usuario)

    # Gera o pdf do certificado
    gerar_certificado_com_pdf_fundo(nome, curso, carga_horaria, data_certificacao, data_emissao, codigo, "modelo.pdf", "certificado.pdf")

    # Sobe o certificado no storage do Supabase e armazena a url
    url = subir_pdf_para_supabase(client, "certificado.pdf", f"{codigo}_{nome}_certificacao_financeiro_basico.pdf")

    # Atualiza o certificado no banco com a url
    atualizar_url_certificado(client, codigo, url)

    # Enviar certificado por e-mail para o(a) estudante
    enviar_certificado_por_email(nome, email, "certificado.pdf", codigo)

    # Aqui você pode processar e armazenar os dados recebidos
    return {"status": "ok"}