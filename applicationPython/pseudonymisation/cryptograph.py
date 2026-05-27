from cryptography.fernet import Fernet
import hashlib

class Crypto : 
    def __init__(self, key) : 
        # Avant de stocker la "clé", on va d'abord vérifier si elle est au format attendu
        if type(key) != bytes : 
            raise TypeError("La clé doit être au format 'bytes' (ou en français : octets)")

        # Le paramètre key doit être de type "bytes" (octets) obtenu uniquement lorsqu'il est généré par Fernet.generate_key()
        self._fernet = Fernet(key)
        # Le underscore avant fernet signifie que cet attribut est protégé (ne peut pas être modifié)

    def encrypt(self, data) : 
        """Fonction de chiffrement des données"""
        # Encodage des données en octet car Fernet ne comprend rien d'autre
        dataBytes = data.encode('utf-8')
        # Chiffrement des octets obtenus afin de chiffrer les données au final
        self.encryptedDatas = self._fernet.encrypt(dataBytes)
        return self.encryptedDatas

    def decrypt(self, encryptedDatas) : 
        """Fonction de déchiffrement des données"""
        # Littéralement la fonction inverse de encrypt(self, data)
        self.decryptedDatas = self._fernet.decrypt(encryptedDatas)
        data = self.decryptedDatas.decode('utf-8')
        return data
    
    def hash(self, data) : 
        """Fonction de hachage SHA-256 des données"""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        hashed_data = sha256_hash.hexdigest()
        return hashed_data

