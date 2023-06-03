import hashlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class FileChangeHandler:
    def __init__(self, private_key):
        self.private_key = private_key

    def on_modified(self, file_path):
        if self.is_supported_file(file_path):
            self.sign_file(file_path)

    def on_deleted(self, file_path):
        if self.is_supported_file(file_path):
            self.remove_signature(file_path)

    def is_supported_file(self, file_path):
        supported_extensions = ['.txt', '.doc', '.pdf']
        file_ext = os.path.splitext(file_path)[1]
        return file_ext in supported_extensions

    def sign_file(self, file_path):
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

        # Firmar el archivo
        signature = self.generate_rsa_signature(private_key, file_path)

        # Guardar la firma en un archivo
        signature_path = self.get_signature_path(file_path)
        with open(signature_path, "wb") as f:
            f.write(signature)

        print(f"El archivo {file_path} ha sido firmado correctamente.")

    def remove_signature(self, file_path):
        signature_path = self.get_signature_path(file_path)
        if os.path.exists(signature_path):
            os.remove(signature_path)
            print(f"La firma del archivo {file_path} ha sido eliminada.")

    def generate_rsa_signature(self, private_key, file_path):
        file_hash = self.calculate_file_hash(file_path)
        signature = private_key.sign(
            file_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def calculate_file_hash(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hasher.update(chunk)
        return hasher.digest()

    def get_signature_path(self, file_path):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        signature_path = f"{file_name}.sig"
        return signature_path


# Generar un par de claves RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Ruta del archivo donde se guardará la clave pública en formato PEM
public_key_path = "public_key.pem"

# Guardar la clave pública en formato PEM en el archivo
with open(public_key_path, "wb") as f:
    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    f.write(public_key_pem)

# Ruta del directorio a firmar
directory_path = 'path/to/directory'


def sign_directory(private_key, directory_path):
    file_change_handler = FileChangeHandler(private_key)
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_change_handler.on_modified(file_path)


# Firmar el directorio
sign_directory(private_key, directory_path)
