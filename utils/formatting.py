
def formatear_mensaje(oferta):
    """
    Formatea una oferta para enviarla bonito a Telegram
    """
    titulo = oferta.get('titulo', 'Sin título')
    precio = oferta.get('precio', 'Precio no disponible')
    ubicacion = oferta.get('ubicacion', 'Ubicación no disponible')
    url = oferta.get('url', '#')

    mensaje = f"""🚐 *{titulo}*
💶 {precio}
📍 {ubicacion}
🔗 [Ver anuncio]({url})
"""
    return mensaje
