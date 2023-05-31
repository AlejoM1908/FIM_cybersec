import os
import hashlib
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generate_rsa_signature(private_key, data):
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.digest()


def sign_directory(private_key, directory_path):
    file_hashes = []
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_file_hash(file_path)
            file_hashes.append(file_hash)

    directory_hash = hashlib.sha256(b''.join(file_hashes)).digest()
    signature = generate_rsa_signature(private_key, directory_hash)
    return signature


# Generar un par de claves RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Obtener la clave pública
public_key = private_key.public_key()

# Ruta del archivo donde se guardará la clave pública en formato PEM
public_key_path = "public_key.pem"

# Guardar la clave pública en formato PEM en el archivo
with open(public_key_path, "wb") as f:
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    f.write(public_key_pem)

# Ruta del directorio a firmar
directory_path = 'D:/GUYAN/Universidad/SEMESTRE_XIII/CIBERSEGURIDAD/ProyectoFinal/FIM_cybersec/tests'

# Firmar el directorio
signature = sign_directory(private_key, directory_path)

# Guardar la firma en un archivo
with open("signature.bin", "wb") as f:
    f.write(signature)

print("El directorio ha sido firmado correctamente.")