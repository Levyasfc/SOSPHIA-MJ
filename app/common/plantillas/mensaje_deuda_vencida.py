from app.common.plantillas.Plantillabase import base_template

def mensaje_deuda_vencida(propietario, deuda):
    titulo = "Aviso de deuda vencida"
    contenido = f"""
Hola {propietario.nombre},

Le informamos que la deuda con vencimiento el {deuda.fecha_limite.strftime('%d/%m/%Y')} 
por valor de ${deuda.valor_total:,.2f} aún no ha sido cancelada.

Por favor comuníquese con la administración para evitar acciones jurídicas.
"""
    return titulo, base_template(titulo, contenido)
