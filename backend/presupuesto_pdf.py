"""Generacion de PDF de presupuesto por obra (acentos latinos preservados)."""

from __future__ import annotations

from fpdf import FPDF

# Helvetica core font: latin-1. Mapeamos caracteres fuera de rango a equivalentes.
_LATIN_MAP = str.maketrans(
    {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
        "ñ": "n",
        "Ñ": "N",
        "ü": "u",
        "Ü": "U",
        "¿": "?",
        "¡": "!",
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "°": " deg",
        "²": "2",
        "³": "3",
    }
)


def _pdf_text(s: object, max_len: int = 500) -> str:
    t = str(s if s is not None else "").translate(_LATIN_MAP)
    # Queda latin-1 seguro para Helvetica (sin '?').
    return t.encode("latin-1", "replace").decode("latin-1")[:max_len]


def build_project_pdf_bytes(project, processes: list) -> bytes:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(14, 14, 14)
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _pdf_text(f"Presupuesto - {project.name}"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    if project.client:
        pdf.cell(0, 6, _pdf_text(f"Cliente: {project.client}"), new_x="LMARGIN", new_y="NEXT")
    if project.address:
        pdf.cell(0, 6, _pdf_text(f"Direccion: {project.address}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    for proc in processes:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, _pdf_text(f"{proc.tipo_plano} - {proc.filename}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, _pdf_text(f"Fecha: {proc.created_at.isoformat()}"), new_x="LMARGIN", new_y="NEXT")
        if proc.escala_detectada is not None:
            pdf.cell(0, 5, _pdf_text(f"Escala detectada (m): {proc.escala_detectada}"), new_x="LMARGIN", new_y="NEXT")
        meta = getattr(proc, "result_meta", None) or {}
        if meta.get("sistema_muro"):
            pdf.cell(0, 5, _pdf_text(f"Sistema muro: {meta.get('sistema_muro')}"), new_x="LMARGIN", new_y="NEXT")
        if meta.get("altura_muro"):
            pdf.cell(0, 5, _pdf_text(f"Altura muro: {meta.get('altura_muro')} m"), new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, _pdf_text(f"Total modulo (ARS): {float(proc.total or 0):.2f}"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 8)
        for item in proc.items or []:
            nom = _pdf_text(item.get("nom", ""), 120)
            val = item.get("val", "")
            line = f" - {nom}: {_pdf_text(val, 80)}"
            pdf.multi_cell(0, 4, line)
        pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    total = sum(float(p.total or 0) for p in processes if getattr(p, "tipo_plano", "") != "terreno")
    pdf.cell(0, 8, _pdf_text(f"Total estimado obra (sin terrenos): ARS {total:.2f}"), new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
