import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet

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


def get_messages_fernet(id1, id2, MASTER_KEY):
	'''renvoie l'objet fernet créé avec la clé unique pour la disscussion entre user1 et user2 (prend les id des utilisateurs en entrée)'''
	# pour encrypter les messages entre user1 et user2
	messages_seed = str(id1) + str(id2)
	messages_key = generate_fernet_key(MASTER_KEY, messages_seed)
	messages_fernet = Fernet(messages_key)
	return messages_fernet


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
