import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="vaccine.py — Detector de inyecciones SQL"
    )
    parser.add_argument(
        "url",
        help='URL objetivo con parámetros, ej: "http://localhost/dvwa/...?id=1&Submit=Submit"',
    )
    parser.add_argument(
        "-X", "--method",
        default="GET",
        choices=["GET", "POST"],
        help="Método HTTP a usar (por defecto: GET)",
    )
    parser.add_argument(
        "-o", "--output",
        default="output/results.txt",
        help="Fichero donde guardar los resultados (por defecto: output/results.txt)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Muestra información detallada de requests y detección",
    )
    return parser.parse_args()
