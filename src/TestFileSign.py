import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def verify_file_signature(public_key, file_path, signature):
    file_hash = calculate_file_hash(file_path)
    valid_signature = verify_rsa_signature(public_key, file_hash, signature)
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


# Ruta del archivo de clave pública
public_key_path = 'public_key.pem'

# Cargar la clave pública
with open(public_key_path, "rb") as f:
    public_key_pem = f.read()
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )

# Ruta del archivo a verificar
file_path = 'D:/GUYAN/Universidad/SEMESTRE_XIII/CIBERSEGURIDAD/ProyectoFinal/FIM_cybersec/tests/ETHEREUM_GUION.pdf'

# Cargar la firma desde el archivo
with open("signature.bin", "rb") as f:
    signature = f.read()

# Verificar la firma del archivo
valid_signature = verify_file_signature(public_key, file_path, signature)

if valid_signature:
    print("La firma del archivo es válida.")
else:   
    print("La firma del archivo no es válida.")
