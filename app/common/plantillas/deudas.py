from app.common.plantillas.Plantillabase import base_template

def mensaje_deuda(usuario, deuda):
    titulo = "Nueva deuda registrada"

    # Hacer seguro si faltan campos
    nombre = usuario.get("nombre", "Propietario")
    apellido = usuario.get("apellido", "")

    contenido = f"""
Hola {nombre} {apellido},

Se ha registrado una nueva deuda a su nombre:

💲 Monto: {deuda.valor_total}
📌 Concepto: {deuda.descripcion or 'Sin descripción'}
📅 Fecha Límite: {deuda.fecha_vencimiento}

Por favor realice el pago lo antes posible para evitar intereses o sanciones.

Saludos cordiales,  
Administración PH
"""

    return base_template(titulo, contenido)
