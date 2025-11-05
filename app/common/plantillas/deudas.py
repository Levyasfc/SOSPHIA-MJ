from app.common.plantillas.Plantillabase import base_template

def mensaje_deuda(propietario, deuda):
    titulo = "Nueva deuda registrada"

    contenido = f"""
Hola {propietario.nombre},

Se ha registrado una nueva deuda a su nombre:

💲 Monto: {deuda.valor_total}
📌 Concepto: {deuda.descripcion or 'Sin descripción'}
📅 Fecha Límite: {deuda.fecha_vencimiento}

Por favor realice el pago lo antes posible para evitar intereses o sanciones.

Saludos cordiales,  
Administración PH
"""

    return base_template(titulo, contenido)
