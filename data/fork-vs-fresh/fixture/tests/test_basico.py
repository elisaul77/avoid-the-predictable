from tienda.factura import resumen


def test_resumen_cuenta_lineas():
    assert resumen([("ARZ01", 1), ("VIN04", 2)])["lineas"] == 2
