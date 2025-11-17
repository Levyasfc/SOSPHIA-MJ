def correo_nuevo_caso(caso, usuario):
    return f"""
    <h2>📄 Nuevo Caso Jurídico Registrado</h2>
    <p><b>Título:</b> {caso.titulo}</p>
    <p><b>Descripción:</b> {caso.descripcion or 'Sin descripción'}</p>
    <p><b>Registrado por:</b> {usuario}</p>
    <p><b>Estado inicial:</b> {caso.estado}</p>
    <hr>
    <p>Fecha: {caso.fecha_creacion}</p>
    """


def correo_nuevo_historial(caso, historial):
    return f"""
    <h2>📌 Nuevo movimiento en tu caso jurídico</h2>
    <p>Se ha añadido una actualización al caso <b>{caso.titulo}</b></p>
    <p><b>Descripción:</b> {historial.descripcion}</p>
    <p><b>Registrado por:</b> {historial.usuario}</p>
    <hr>
    <p>Fecha: {historial.fecha}</p>
    """


def correo_estado_actualizado(caso, nuevo_estado):
    return f"""
    <h2>📢 Actualización de Estado del Caso</h2>
    <p>El caso <b>{caso.titulo}</b> ha cambiado su estado.</p>
    <p><b>Nuevo estado:</b> {nuevo_estado}</p>
    <hr>
    <p>Fecha: {caso.fecha_creacion}</p>
    """
