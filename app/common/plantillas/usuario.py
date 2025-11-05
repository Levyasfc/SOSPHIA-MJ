from app.common.plantillas.Plantillabase import base_template

def mensaje_nuevo_propietario(propietario):
    contenido = f"""
¡Bienvenido a la plataforma de Propiedad Horizontal!

Se ha registrado tu usuario exitosamente.

👤 Nombre: {propietario.nombre} 
🏠 Unidad / Propiedad: {propietario.propiedadID or 'No registrada'}
📧 Correo: {propietario.correo}

Desde ahora podrás recibir notificaciones importantes sobre tu propiedad y la copropiedad.

Gracias por pertenecer a nuestra comunidad.
"""
    return base_template("Bienvenido a la plataforma", contenido)
