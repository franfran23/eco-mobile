import base64
from flask import make_response, redirect
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet, InvalidToken

def generate_fernet_key(master_key, seed):
    # Créer un HKDF avec SHA256 comme fonction de hachage
    # la seed correspond à quelle clé générer, ex: clé de cryptage pour les cookies
    data = master_key.encode('utf-8')
    salt = seed.encode('utf-8')
    
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # Longueur de la clé de chiffrement AES (256 bits)
        salt=salt,
        info=None,
        backend=default_backend()
    )

    # Dérivation de la clé de chiffrement à partir de la clé maître
    derived_key = hkdf.derive(data)

    return base64.urlsafe_b64encode(derived_key).decode()

# TEST UNIT
'''
MASTER_KEY = 'clé'
seed = 'messages'
print('MASTER_KEY', MASTER_KEY)
print('seed', seed)
key = generate_fernet_key(MASTER_KEY, seed)
print('derived_key', key)
fernet = Fernet(key)
print('fernet object', fernet)
'''

def get_messages_fernet(id1, id2, MASTER_KEY):
	'''renvoie l'objet fernet créé avec la clé unique pour la disscussion entre user1 et user2 (prend les id des utilisateurs en entrée)'''
	# pour encrypter les messages entre user1 et user2
	messages_seed = str(id1) + str(id2)
	messages_key = generate_fernet_key(MASTER_KEY, messages_seed)
	messages_fernet = Fernet(messages_key)
	return messages_fernet

def get_cookies_fernet(MASTER_KEY):
	'''renvoie l'élément de cryptage fernet pour les cookies'''
	cookies_seed = 'cookies' # graine de génération de la clé de cryptage des cookies # on définira une vraie clé plus tard # une nouvelle clé déconnectera toutes les sessions utilisateurs en cours
	cookies_key = generate_fernet_key(MASTER_KEY, cookies_seed) # clé de cryptage des cookies
	cookies_fernet = Fernet(cookies_key)
	return cookies_fernet

COOKIE_NAME = "cookies" # temporaire
def store_session_cookie(username, MASTER_KEY):
	cookies_fernet = get_cookies_fernet(MASTER_KEY)
	
	response = make_response(redirect('/?message=Login Successful'))
	response.set_cookie(COOKIE_NAME, cookies_fernet.encrypt(username.encode('utf-8')).decode('utf-8'), secure=True, httponly=True)
	return response

def remove_cookie(response):
	response.delete_cookie(COOKIE_NAME)
