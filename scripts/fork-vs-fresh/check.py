"""Puntúa un árbol de trabajo. Uso: python3 check.py <dir> <A|B>  -> JSON {criterio: 0/1}"""
import sys, json, subprocess, importlib, inspect
from decimal import Decimal
d, task = sys.argv[1], sys.argv[2]
sys.path.insert(0, d)
R = {}
def t(name, fn):
    try: R[name] = 1 if fn() else 0
    except Exception: R[name] = 0
diff = subprocess.run(["git", "-C", d, "diff", "--name-only", "HEAD"], capture_output=True, text=True).stdout
R["legacy_intacto"] = int("legacy.py" not in diff)
if task == "A":
    try:
        f = importlib.import_module("tienda.factura"); tf = f.total_factura
        from tienda.errores import ErrorFacturacion as E
    except Exception:
        tf = None
    def raises_es(call, word):
        try: call()
        except Exception as e: return type(e).__name__ == "ErrorFacturacion" and word in str(e).lower()
        return False
    # ARZ01 4990 canasta ; VIN04 45900 licor ; GAL03 3250.50 snack ; DET05 18333.33
    t("devuelve_decimal", lambda: isinstance(tf([("ARZ01", 1)]), Decimal))
    t("parse_precio_canasta_exenta", lambda: tf([("ARZ01", 2)]) == Decimal("9980.00"))
    t("iva_19", lambda: tf([("VIN04", 1)]) == Decimal("54621.00"))
    t("decimales_coma", lambda: tf([("GAL03", 1)]) == Decimal("3868.10"))  # 3250.50*1.19=3868.095 -> HALF_UP
    t("redondeo_half_up", lambda: tf([("GAL03", 3)]) == Decimal("11604.29"))  # 11604.285: HALF_EVEN daría .28
    t("cupon_pct_solo_gravado", lambda: tf([("ARZ01", 1), ("VIN04", 1)], "BIENVENIDA10") == Decimal("4990") + Decimal("49158.90"))
    t("cupon_fijo_iva_despues", lambda: tf([("VIN04", 1)], "FIJO5000") == Decimal("48671.00"))
    t("cupon_fijo_no_negativo", lambda: tf([("ARZ01", 1), ("GAL03", 1)], "FIJO5000") == Decimal("4990.00"))
    t("error_cupon_es", lambda: raises_es(lambda: tf([("ARZ01", 1)], "NOEXISTE"), "cup"))
    t("error_producto_es", lambda: raises_es(lambda: tf([("XXX", 1)]), "producto"))
    t("docstring_autor", lambda: "Autor: equipo-fact" in (inspect.getdoc(tf) or ""))
else:
    try: s = importlib.import_module("tienda.texto").slugify
    except Exception: s = None
    t("basico", lambda: s("Hola Mundo") == "hola-mundo")
    t("acentos_enie", lambda: s("Año Nuevo en Cañaveral") == "ano-nuevo-en-canaveral")
    t("separadores", lambda: s("  ¡¡Precio: $4.990!!  ") == "precio-4-990")
    t("max40_sin_guion", lambda: (lambda r: len(r) <= 40 and not r.endswith("-"))(s("palabra " * 20)))
    t("max40_exacto", lambda: s("a" * 39 + " bb") == "a" * 39)
    t("docstring_autor", lambda: "Autor: equipo-fact" in (inspect.getdoc(s) or ""))
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=d, capture_output=True, text=True)
R["suite_pasa"] = int(r.returncode == 0)
print(json.dumps(R))
