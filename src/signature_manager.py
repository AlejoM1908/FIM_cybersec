import hashlib
import os
import random
import string
from typing import Tuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class SignatureManager:
    '''
        This class is responsible for managing the signatures of the files and directories in track.
    '''
    def __init__(self) -> None:
        '''
            This method is responsible for initializing the class.

            @param {bool} use_passphrase: If the passphrase should be used or not.
        '''
        self._passphrase = None

    def _generatePrivateKey(self) -> rsa.RSAPrivateKey:
        '''
            This method is responsible for generating the private key.

            Return the private key.
        '''
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        return private_key

    def _generatePublicKey(self, private_key:rsa.RSAPrivateKey) -> rsa.RSAPublicKey:
        '''
            This method is responsible for generating the public key.

            @param {rsa.RSAPrivateKey} private_key: The private key to generate the public key.

            Returnn the public key.
        '''
        public_key = private_key.public_key()

        return public_key
    
    def _serializeKey(self, key: rsa.RSAPrivateKey | rsa.RSAPublicKey, *, is_private:bool = False) -> bytes:
        '''
            This method is responsible for serializing the key.

            @param {rsa.RSAPrivateKey | rsa.RSAPublicKey} key: The key to serialize.
            @param {bool} is_private: If the key is private or not.

            Return the serialized key, if it is private, it will be encrypted as well.

            @raise {TypeError}: If the key is not a private or public key.
        '''
        if is_private:
            encryption_algo = serialization.BestAvailableEncryption(self._passphrase) if self._passphrase is not None else serialization.NoEncryption()

            if isinstance(key, rsa.RSAPrivateKey):
                key_bytes = key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=encryption_algo
                )
            else: raise TypeError('The key must be a private or public key.'
            )
        else: 
            if isinstance(key, rsa.RSAPublicKey):
                key_bytes = key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            else: raise TypeError('The key must be a private or public key.')

        return key_bytes
    
    def _deserializeKey(self, key_bytes:bytes, *, is_private:bool = False) -> rsa.RSAPrivateKey | rsa.RSAPublicKey:
        '''
            This method is responsible for deserializing the key.

            @param {bytes} key_bytes: The key to deserialize.
            @param {bool} is_private: If the key is private or not.

            Return the deserialized key, if it is private, it will be decrypted as well.

            @raise {ValueError}: If the key doesn't have a valid format.
        '''
        if is_private:
            return serialization.load_pem_private_key(
                key_bytes,
                password=self._passphrase,
            )
        else:
            return serialization.load_pem_public_key(
                key_bytes
            )

    def _calculateFileHash(self, path:str) -> bytes:
        '''
            This method is responsible for calculating the hash of the file.

            @param {str} path: The path of the file.

            Return the binary hash of the file.

            @raise {FileNotFoundError}: If the file does not exist.
        '''
        hasher = hashlib.sha256()

        with open(path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hasher.update(chunk)

        return hasher.digest()
    
    def _calculateDirectoryHash(self, path:str) -> bytes:
        '''
            This method is responsible for calculating the hash of the directory.

            @param {str} path: The path of the directory.

            Return the binary hash of the directory.

            @raise {FileNotFoundError}: If the directory does not exist.
        '''
        hasher = hashlib.sha256()

        for root, _, files in os.walk(path):
            for file in files:
                hasher.update(self._calculateFileHash(os.path.join(root, file)))

        return hasher.digest()
    
    def _cypher(self, data:any, pub_key:str) -> bytes:
        '''
            This method is responsible for cyphering the file.

            @param {any} data: The data to cypher.
            @param {str} pub_key: The public key to cypher the data.

            Return the cyphered data.
        '''
        public = self._deserializeKey(pub_key)
        secret = public.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

        return secret
    
    def _decypher(self, data:any, private_key:bytes) -> bytes:
        '''
            This method is responsible for decyphering the file.

            @param {any} data: The data to decypher.
            @param {bytes} private_key: The private key to decypher the data.

            Return the decyphered data.
        '''
        private = self._deserializeKey(private_key, is_private=True)
        decypher = private.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

        return decypher
    
    def validKeyPair(self, private_key:bytes, public_key:bytes) -> bool:
        '''
            This method is responsible for checking if the public key is related to the private key.

            @param {bytes} private_key: The private key to check.
            @param {bytes} plublic_key: The public key to check.

            Return if the public key is related to the private key.
        '''
        try:
            test_message = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters) - 1)] for _ in range(40)])

            secret = self._cypher(bytes(test_message, 'utf-8'), public_key)
            message = self._decypher(secret, private_key)

            return message == bytes(test_message, 'utf-8')
        except:
            return False
    
    def setPassphrase(self, passphrase:str) -> None:
        '''
            This method is responsible for setting the passphrase.

            @param {str} passphrase: The passphrase to set.
        '''
        if passphrase is None: self. _passphrase = None
        else: self._passphrase = bytes(passphrase, 'utf-8')

    def generateKeyPair(self) -> Tuple[bytes, bytes]:
        '''
            This method is responsible for generating the public and private keys.

            Return the serialized private and public keys in a tuple formated like [private, public].
        '''
        private_key = self._generatePrivateKey()
        public_key = self._generatePublicKey(private_key)

        return self._serializeKey(private_key, is_private=True), self._serializeKey(public_key)

    def sign(self, private_key:bytes, file_path:bytes, *, is_directory:bool = False) -> bytes:
        '''
            This method is responsible for signing the file or directory in track.

            @param {bytes} private_key: The private key to sign the file or directory.
            @param {str} file_path: The path of the file or directory to sign.
            @param {bool} is_directory: If the path is a directory or not.

            Return the signature of the file or directory.

            @raise {FileNotFoundError}: If the file or directory does not exist.
        '''
        private = self._deserializeKey(private_key, is_private=True)

        path_hash = self._calculateDirectoryHash(file_path) if is_directory else self._calculateFileHash(file_path)

        signature = private.sign(path_hash, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

        return signature

    def verifySignature(self, public_key:str, signature:str, file_path:str, *, is_directory:bool = False) -> bool:
        '''
            This method is responsible for verifying the signature of the file or directory in track.

            @param {str} public_key: The public key to verify the signature.
            @param {str} signature: The signature to verify.
            @param {str} file_path: The path of the file or directory to verify.
            @param {bool} is_directory: If the path is a directory or not.

            Return if the signature is valid or not.

            @raise {FileNotFoundError}: If the file or directory does not exist.
        '''
        public = self._deserializeKey(public_key)

        path_hash = self._calculateDirectoryHash(file_path) if is_directory else self._calculateFileHash(file_path)

        try:
            public.verify(signature, path_hash, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
            
            return True
        except:
            return False
        
    