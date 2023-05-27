import os
import hashlib
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def verify_directory_signature(public_key, directory_path, signature):
    file_hashes = []
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_file_hash(file_path)
            file_hashes.append(file_hash)

    directory_hash = hashlib.sha256(b''.join(file_hashes)).digest()
    valid_signature = verify_rsa_signature(public_key, directory_hash, signature)
    return valid_signature


def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.digest()


def verify_rsa_signature(public_key, data, signature):
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


# Ruta del archivo de clave pública (public_key.pem)
public_key_path = 'public_key.pem'

# Cargar la clave pública desde el archivo
with open(public_key_path, "rb") as f:
    public_key_pem = f.read()
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )

# Ruta del directorio a verificar
directory_path = 'D:/GUYAN/Universidad/SEMESTRE_XIII/CIBERSEGURIDAD/ProyectoFInal/FIM_cybersec/tests'

# Cargar la firma desde el archivo
with open("signature.bin", "rb") as f:
    signature = f.read()

# Verificar la firma del directorio
valid_signature = verify_directory_signature(public_key, directory_path, signature)

if valid_signature:
    print("La firma del directorio es válida.")
else:   
    print("La firma del directorio no es válida.")
