from app.common.plantillas.Plantillabase import base_template


def mensaje_poder_otorgado(otorgante: dict, apoderado: dict, poder):
    nombre_otorgante = otorgante["person"]["first_name"]
    apellido_otorgante = otorgante["person"]["last_name"]

    nombre_apoderado = apoderado["person"]["first_name"]
    apellido_apoderado = apoderado["person"]["last_name"]

    titulo = "📄 Se te ha otorgado un poder"

    contenido = f"""
Hola {nombre_apoderado} {apellido_apoderado},

Has sido asignado como **apoderado** por:

👤 **{nombre_otorgante} {apellido_otorgante}**

Detalles del poder:

- 🗓 Fecha otorgado: {poder.fecha_otorgado}
- 📅 Fecha expiración: {poder.fecha_expiracion or 'Sin fecha de expiración'}
- 🏢 Conjunto Residencial ID: {poder.hp_id}

Este poder te autoriza a representar al otorgante en procesos administrativos.

Saludos,
Administración PH
"""

    return base_template(titulo, contenido)