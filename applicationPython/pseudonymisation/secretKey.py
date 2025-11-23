# La clé secrète sera celle-ci
secretKey = b'I2Svw7X7C86fjn_rKcbMF6GG2WJfPH6nP47r-yRFHTU='

""" # Génération d'une clé secrète (à exécuter une seule fois)
from cryptography.fernet import Fernet
secretKey = Fernet.generate_key()
"""

# Pour des jeux de tests :
# chiffrement = Crypto(secretKey)
# donneesChiffrees = chiffrement.encrypt( <Données à chiffrées> )
# donneesDechiffrees = chiffrement.decrypt( donneesChiffrees)