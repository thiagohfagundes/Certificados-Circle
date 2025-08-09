import requests, os
from dotenv import load_dotenv

load_dotenv()

def dados_do_usuario_circle(id):
  """Retorna os dados do usuário Circle a partir do ID."""
  url = f"https://app.circle.so/api/admin/v2/community_members/{id}"

  token_circle = os.getenv('TOKEN_CIRCLE')

  headers = {
      "Authorization": f"Bearer {token_circle}",
      "Content-Type": "application/json"
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      data = response.json()
      return data
  else:
      print(f"Erro na solicitação. Código de status: {response.status_code}")

def recebe_webhook_e_captura_nome(event):
  """Recebe um webhook do Circle e retorna o nome do membro da comunidade."""
  return event['data']['community_member_id']