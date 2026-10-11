from .catalogo import PRODUCTOS
from .legacy import subtotal


def resumen(items):
    """Resumen rápido para la vista de carrito."""
    return {"lineas": len(items), "subtotal": subtotal(items, PRODUCTOS)}
