from typing import Tuple
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import hashlib
import os

class SignatureManager:
    '''
        This class is responsible for managing the signatures of the files and directories in track.
    '''
    def __init__(self, passphrase) -> None:
        self.passphrase = passphrase

    def _generate_private_key(self) -> rsa.RSAPrivateKey:
        '''
            This method is responsible for generating the private key.
        '''
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        return private_key

    def _generate_public_key(self, private_key:rsa.RSAPrivateKey) -> rsa.RSAPublicKey:
        '''
            This method is responsible for generating the public key.
        '''
        public_key = private_key.public_key()

        return public_key
    
    def _serialize_key(self, key:rsa.RSAPrivateKey | rsa.RSAPublicKey, *, is_private:bool = False) -> bytes:
        '''
            This method is responsible for serializing the key.
        '''
        if is_private:
            key_bytes = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(self.passphrase)
            )
        else:
            key_bytes = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

        return key_bytes
    
    def _deserialize_key(self, key_bytes:bytes, *, is_private:bool = False) -> rsa.RSAPrivateKey | rsa.RSAPublicKey:
        '''
            This method is responsible for deserializing the key.
        '''
        if is_private:
            key = serialization.load_pem_private_key(
                key_bytes,
                password=self.passphrase
            )
        else:
            key = serialization.load_pem_public_key(
                key_bytes
            )

        return key

    def _calculate_file_hash(self, path:str) -> bytes:
        '''
            This method is responsible for calculating the hash of the file.
        '''
        hasher = hashlib.sha256()

        with open(path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hasher.update(chunk)

        return hasher.digest()
    
    def _calculate_directory_hash(self, path:str) -> bytes:
        '''
            This method is responsible for calculating the hash of the directory.
        '''
        hasher = hashlib.sha256()

        for root, _, files in os.walk(path):
            for file in files:
                hasher.update(self._calculate_file_hash(os.path.join(root, file)))

        return hasher.digest()

    def generate_key_pair(self) -> Tuple[bytes, bytes]:
        '''
            This method is responsible for generating the public and private keys.
        '''
        private_key = self._generate_private_key()
        public_key = self._generate_public_key(private_key)

        return self._serialize_key(private_key, is_private=True), self._serialize_key(public_key)

    def sign(self, private_key:bytes, file_path:bytes, *, is_directory:bool = False) -> bytes:
        '''
            This method is responsible for signing the file or directory in track.
        '''
        private = self._deserialize_key(private_key, is_private=True)

        path_hash = self._calculate_directory_hash(file_path) if is_directory else self._calculate_file_hash(file_path)

        signature = private.sign(path_hash, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

        return signature

    def verify(self, pub_key:str, signature:str, file_path:str, *, is_directory:bool = False) -> bool:
        '''
            This method is responsible for verifying the signature of the file or directory in track.
        '''
        public = self._deserialize_key(pub_key)

        path_hash = self._calculate_directory_hash(file_path) if is_directory else self._calculate_file_hash(file_path)

        try:
            public.verify(signature, path_hash, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        except:
            return False
        
        return True