import os
import sys
import unittest
from cryptography.hazmat.primitives import serialization

sys.path.insert(0, os.path.abspath('..'))
from src.signature_manager import SignatureManager


class TestSignatureManager(unittest.TestCase):
    def setUp(self):
        self.signature_manager = SignatureManager()

    def test_generateKeyPair(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()

        # Process
        # Assertions
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)

    def test_serializeKey(self):
        # Varibles
        private = self.signature_manager._generatePrivateKey()
        public = self.signature_manager._generatePublicKey(private)
        self.signature_manager.setPassphrase('test')

        # Process
        serialized_private = self.signature_manager._serializeKey(private, is_private=True)
        serialized_public = self.signature_manager._serializeKey(public)

        # Assertions
        self.assertIsInstance(serialized_private, bytes)
        self.assertIsInstance(serialized_public, bytes)

    def test_deserializeKey(self):
        # Varibles
        private = self.signature_manager._generatePrivateKey()
        public = self.signature_manager._generatePublicKey(private)
        self.signature_manager.setPassphrase('test')

        # Process
        serialized_private = self.signature_manager._serializeKey(private, is_private=True)
        serialized_public = self.signature_manager._serializeKey(public)

        deserialized_private = self.signature_manager._deserializeKey(serialized_private, is_private=True)
        deserialized_public = self.signature_manager._deserializeKey(serialized_public)

        # Assertions
        self.assertIsInstance(deserialized_private, object)
        self.assertIsInstance(deserialized_public, object)

    def test_sign(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()

        # Process
        signature = self.signature_manager.sign(private_key, 'tests/test.txt')

        # Assertions
        self.assertIsInstance(signature, bytes)

    def test_verifySignature(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()
        signature = self.signature_manager.sign(private_key, 'tests/test.txt')

        # Process
        is_valid = self.signature_manager.verifySignature(public_key, signature, 'tests/test.txt')

        # Assertions
        self.assertTrue(is_valid)

    def test_verifySignatureWithOtherFile(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()
        signature = self.signature_manager.sign(private_key, 'tests/test.txt')

        # Process
        is_valid = self.signature_manager.verifySignature(public_key, signature, 'tests/test2.txt')

        # Assertions
        self.assertFalse(is_valid)

    def test_verifySignatureWithWrongPublicKey(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()
        signature = self.signature_manager.sign(private_key, 'tests/test.txt')

        # Process
        # Assertions
        with self.assertRaises(ValueError):
            self.signature_manager.verifySignature(b'123', signature, 'tests/test.txt')

    def test_verifySignatureWithWrongSignature(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()
        signature = self.signature_manager.sign(private_key, 'tests/test.txt')

        # Process
        is_valid = self.signature_manager.verifySignature(public_key, b'123', 'tests/test.txt')

        # Assertions
        self.assertFalse(is_valid)

    def test_verifySignatureWithUnexistantFile(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()
        signature = self.signature_manager.sign(private_key, 'tests/test.txt')

        # Process
        # Assertions
        with self.assertRaises(FileNotFoundError):
            self.signature_manager.verifySignature(public_key, signature, 'tests/test3.txt')

    def test_verifySignatureWithEmptyFile(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()
        signature = self.signature_manager.sign(private_key, 'tests/test.txt')

        # Process
        is_valid = self.signature_manager.verifySignature(public_key, signature, 'tests/test_empty.txt')

        # Assertions
        self.assertFalse(is_valid)

    def test_verifyKeyIntegrityAfterSerialization(self):
        # Varibles
        private_key = self.signature_manager._generatePrivateKey()
        public_key = self.signature_manager._generatePublicKey(private_key)
        encoding = serialization.Encoding.OpenSSH
        format = serialization.PublicFormat.OpenSSH

        # Process
        serialized_private = self.signature_manager._serializeKey(private_key, is_private=True)
        serialized_public = self.signature_manager._serializeKey(public_key)

        deserialized_private = self.signature_manager._deserializeKey(serialized_private, is_private=True)
        deserialized_public = self.signature_manager._deserializeKey(serialized_public)

        # Assertions
        self.assertEqual(private_key.public_key().public_bytes(encoding, format), deserialized_private.public_key().public_bytes(encoding, format))
        self.assertEqual(public_key.public_bytes(encoding, format), deserialized_public.public_bytes(encoding, format))

    def test_verifyPrivateKeySerializationEncryption(self):
        # Varibles
        self.signature_manager.setPassphrase('test')
        private_key, public_key = self.signature_manager.generateKeyPair()

        # Process
        self.signature_manager.setPassphrase('OtherPassphrase')

        # Assertions
        with self.assertRaises(ValueError):
            self.signature_manager._deserializeKey(private_key, is_private=False)

def start_test():
    unittest.main()

if __name__ == '__main__':
    start_test()