from app.common.plantillas.Plantillabase import base_template

def mensaje_nueva_asamblea(asamblea):
    contenido = f"""
Se ha programado una nueva Asamblea:

🗓 Fecha: {asamblea.fecha}
📍 Lugar: {asamblea.lugar}
📝 Descripción: {asamblea.descripcion or 'Sin descripción'}

Por favor estar atento.
"""
    return base_template(f"Nueva Asamblea - {asamblea.tipo}", contenido)
