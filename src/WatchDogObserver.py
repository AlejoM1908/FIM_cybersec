import os
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from watchdog.observers import Observer

from SignsWatchDog import FileChangeHandler

# Ruta del archivo donde se guarda la clave privada en formato PEM
private_key_path = "private_key.pem"
# Ruta del archivo donde se guarda la clave pública en formato PEM
public_key_path = "public_key.pem"

# Verificar si las claves ya existen en el sistema
if not (os.path.exists(private_key_path) and os.path.exists(public_key_path)):
    # Generar un par de claves RSA si no existen
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Obtener la clave pública
    public_key = private_key.public_key()

    # Guardar la clave privada en formato PEM en el archivo
    with open(private_key_path, "wb") as f:
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        f.write(private_key_pem)

    # Guardar la clave pública en formato PEM en el archivo
    with open(public_key_path, "wb") as f:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        f.write(public_key_pem)
else:
    # Cargar la clave privada desde el archivo
    with open(private_key_path, "rb") as f:
        private_key_pem = f.read()
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
        )

    # Cargar la clave pública desde el archivo
    with open(public_key_path, "rb") as f:
        public_key_pem = f.read()
        public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )

# Directorio a monitorear
directory_path = 'path/to/directory'

# Generar una instancia del observador de watchdog
observer = Observer()
event_handler = FileChangeHandler(private_key, public_key)

# Configurar el observador para monitorear cambios en el directorio
observer.schedule(event_handler, directory_path, recursive=True)

# Iniciar el observador
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()