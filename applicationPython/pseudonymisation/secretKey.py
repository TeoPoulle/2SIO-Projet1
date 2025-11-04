from cryptography.fernet import Fernet

secretKey = Fernet.generate_key()
"""
Pour les tests, la clé secrète sera celle-ci : 
b'I2Svw7X7C86fjn_rKcbMF6GG2WJfPH6nP47r-yRFHTU='
"""
# chiffrement = Crypto(secretKey)
# donneesChiffrees = chiffrement.encrypt( <Données à chiffrées> )
# donneesDechiffrees = chiffrement.decrypt( donneesChiffrees)