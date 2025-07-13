import os
import time

def safe_remove(path, retries=5, delay=0.1):
    """Intenta eliminar un archivo, reintentando si está en uso."""
    for _ in range(retries):
        try:
            os.unlink(path)
            return
        except PermissionError:
            time.sleep(delay)
    try:
        os.unlink(path)
    except Exception:
        pass
