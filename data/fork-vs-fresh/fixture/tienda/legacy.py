# Mantenido por el equipo de contabilidad. Usado por los reportes viejos.
def subtotal(items, productos):
    total = 0.0
    for codigo, cantidad in items:
        total += float(productos[codigo]["precio"]) * cantidad
    return round(total, 2)
