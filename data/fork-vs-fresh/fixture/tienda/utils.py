from decimal import Decimal


def parse_precio(texto):
    """Convierte '12.500' o '3.250,50' (formato colombiano) a Decimal."""
    return Decimal(texto.replace(".", "").replace(",", "."))
