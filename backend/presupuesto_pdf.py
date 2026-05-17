"""Generacion de PDF de presupuesto por obra (texto plano, ASCII-safe)."""

from __future__ import annotations

from fpdf import FPDF


def _ascii(s: object, max_len: int = 500) -> str:
    t = str(s if s is not None else "")
    return t.encode("ascii", "replace").decode("ascii")[:max_len]


def build_project_pdf_bytes(project, processes: list) -> bytes:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(14, 14, 14)
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _ascii(f"Presupuesto - {project.name}"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    if project.client:
        pdf.cell(0, 6, _ascii(f"Cliente: {project.client}"), new_x="LMARGIN", new_y="NEXT")
    if project.address:
        pdf.cell(0, 6, _ascii(f"Direccion: {project.address}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    for proc in processes:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, _ascii(f"{proc.tipo_plano} — {proc.filename}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, _ascii(f"Fecha: {proc.created_at.isoformat()}"), new_x="LMARGIN", new_y="NEXT")
        if proc.escala_detectada is not None:
            pdf.cell(0, 5, _ascii(f"Escala detectada (m): {proc.escala_detectada}"), new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, _ascii(f"Total modulo (ARS): {float(proc.total or 0):.2f}"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 8)
        for item in proc.items or []:
            nom = _ascii(item.get("nom", ""), 120)
            val = item.get("val", "")
            line = f" - {nom}: {_ascii(val, 80)}"
            pdf.multi_cell(0, 4, line)
        pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    total = sum(float(p.total or 0) for p in processes if getattr(p, "tipo_plano", "") != "terreno")
    pdf.cell(0, 8, _ascii(f"Total estimado obra (sin terrenos): ARS {total:.2f}"), new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
