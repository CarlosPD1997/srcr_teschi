import base64
import uuid

# Create your views here.
def generar_codigo_unico():
        random_uuid = uuid.uuid4()
    
        # Convertir el UUID a bytes
        uuid_bytes = random_uuid.bytes
        
        # Codificar en Base64 y obtener una cadena
        base64_uuid = base64.urlsafe_b64encode(uuid_bytes).decode('utf-8')
        
        # Tomar los primeros 8 caracteres
        codigo_corto = base64_uuid[:8]
        
        return codigo_corto