import datetime
import hashlib


def generar_hash_licencia(fecha: datetime.date, clave_secreta: str) -> str:
    """Calcula el hash de licencia a partir de la fecha de caducidad y la clave secreta."""
    if not clave_secreta or not clave_secreta.strip():
        raise ValueError("La clave secreta no puede estar vacía.")
    combinacion = f"{fecha.strftime('%d/%m/%Y')}:{clave_secreta.strip()}"
    hash_completo = hashlib.sha1(combinacion.encode("utf-8")).hexdigest()
    return hash_completo[:12]
