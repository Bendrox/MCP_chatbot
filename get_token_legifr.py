import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id_prod=os.getenv('client_id_prod')
client_secret_prod=os.getenv('client_secret_prod')


def get_token():
    token_url = 'https://oauth.piste.gouv.fr/api/oauth/token'
    #inject cred 
    token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id_prod,
    'client_secret': client_secret_prod,
    'scope': 'openid'}
    response = requests.post(token_url, data=token_data)
    response.raise_for_status()  # vérif  erreurs
    # récup  jeton
    token_info = response.json()
    access_token = token_info['access_token']
    return access_token