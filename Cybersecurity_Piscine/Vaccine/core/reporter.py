import os


def format_results(url: str, findings: list, extraction=None) -> str:
    lines = [
        "=" * 60,
        f"URL analizada : {url}",
        f"Vulnerabilidades encontradas: {len(findings)}",
    ]
    if findings:
        for f in findings:
            lines.append(f"  [VULNERABLE] Método: {f}")
    else:
        lines.append("  [OK] No se detectaron inyecciones SQL.")

    if extraction is not None:
        lines.append("-" * 60)
        lines.append(f"Parámetros vulnerables: {', '.join(extraction.vulnerable_parameters) if extraction.vulnerable_parameters else 'N/A'}")
        lines.append(f"Payloads usados: {', '.join(extraction.payloads_used) if extraction.payloads_used else 'N/A'}")
        lines.append(f"Motor detectado: {extraction.engine}")
        lines.append(f"Base actual: {extraction.current_db or 'N/A'}")
        lines.append(f"Bases de datos: {', '.join(extraction.databases) if extraction.databases else 'N/A'}")

        if extraction.tables:
            lines.append("Tablas por base:")
            for db_name, tables in extraction.tables.items():
                lines.append(f"  - {db_name}: {', '.join(tables) if tables else 'N/A'}")

        if extraction.columns:
            lines.append("Columnas por tabla:")
            for table_name, columns in extraction.columns.items():
                lines.append(f"  - {table_name}: {', '.join(columns) if columns else 'N/A'}")

        if extraction.dump:
            lines.append("Dump:")
            for table_name, rows in extraction.dump.items():
                lines.append(f"  - {table_name}: {len(rows)} filas")
                for row in rows:
                    lines.append(f"      {row}")

    lines.append("=" * 60)
    return "\n".join(lines)

def save_results(content: str, filepath: str):
    try:
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"[*] Resultados guardados en: {filepath}")
    except IOError as e:
        print(f"[!] No se pudo guardar el fichero: {e}")
