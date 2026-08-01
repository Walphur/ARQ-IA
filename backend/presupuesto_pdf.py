"""Generacion de PDF de presupuesto por obra con Unicode (acentos)."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

_FONTS_DIR = Path(__file__).resolve().parent / "fonts"
_FONT_REG = _FONTS_DIR / "DejaVuSans.ttf"
_FONT_BOLD = _FONTS_DIR / "DejaVuSans-Bold.ttf"

_TIPO_LABEL = {
    "muros": "Estructura y terminaciones",
    "agua": "Instalacion sanitaria y gas",
    "luz": "Instalacion electrica",
    "techo": "Techos y losas",
    "terreno": "Terrenos y lotes",
}


def _txt(s: object, max_len: int = 500) -> str:
    return str(s if s is not None else "")[:max_len]


def _money(value: object) -> str:
    try:
        n = float(value or 0)
    except (TypeError, ValueError):
        return str(value)
    return f"$ {n:,.0f}".replace(",", ".")


class PresupuestoPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "ARQ-IA · Presupuesto de obra", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 8, f"Pagina {self.page_no()}/{{nb}}", align="C")


def build_project_pdf_bytes(project, processes: list) -> bytes:
    if not _FONT_REG.exists() or not _FONT_BOLD.exists():
        raise RuntimeError(
            "Faltan fuentes DejaVu en backend/fonts/. "
            "Incluye DejaVuSans.ttf y DejaVuSans-Bold.ttf para PDF con acentos."
        )

    pdf = PresupuestoPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_margins(14, 14, 14)
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_font("DejaVu", "", str(_FONT_REG))
    pdf.add_font("DejaVu", "B", str(_FONT_BOLD))
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "Presupuesto de obra", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 8, _txt(project.name, 120), new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(60, 60, 60)
    if project.client:
        pdf.cell(0, 6, f"Cliente: {_txt(project.client, 120)}", new_x="LMARGIN", new_y="NEXT")
    if project.address:
        pdf.cell(0, 6, f"Dirección: {_txt(project.address, 160)}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    total_obra = sum(
        float(p.total or 0) for p in processes if getattr(p, "tipo_plano", "") != "terreno"
    )

    for proc in processes:
        tipo = getattr(proc, "tipo_plano", "") or ""
        label = _TIPO_LABEL.get(tipo, tipo)
        pdf.set_fill_color(245, 240, 225)
        pdf.set_font("DejaVu", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, f"{label} — {_txt(proc.filename, 80)}", fill=True, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("DejaVu", "", 9)
        pdf.set_text_color(70, 70, 70)
        pdf.cell(0, 5, f"Fecha: {proc.created_at.isoformat()}", new_x="LMARGIN", new_y="NEXT")
        if proc.escala_detectada is not None:
            pdf.cell(0, 5, f"Escala detectada: {proc.escala_detectada} m", new_x="LMARGIN", new_y="NEXT")
        meta = getattr(proc, "result_meta", None) or {}
        if meta.get("sistema_muro"):
            sistema = "Ladrillo hueco 12 cm" if meta.get("sistema_muro") == "ladrillo_hueco_12" else "Ladrillo común 12 cm"
            pdf.cell(0, 5, f"Sistema: {sistema}", new_x="LMARGIN", new_y="NEXT")
        if meta.get("altura_muro"):
            pdf.cell(0, 5, f"Altura de muro: {meta.get('altura_muro')} m", new_x="LMARGIN", new_y="NEXT")
        if tipo != "terreno":
            pdf.set_font("DejaVu", "B", 9)
            pdf.cell(0, 5, f"Total módulo: {_money(proc.total)} ARS", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(1)
        pdf.set_font("DejaVu", "", 8)
        pdf.set_text_color(40, 40, 40)
        for item in proc.items or []:
            nom = _txt(item.get("nom", ""), 100)
            val = item.get("val", "")
            if tipo == "terreno":
                line = f"• {nom}: {_txt(val, 80)}"
            else:
                line = f"• {nom}: {_money(val)}"
            pdf.multi_cell(0, 4.2, line)
        pdf.ln(3)

    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(0.4)
    pdf.line(14, pdf.get_y(), 196, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("DejaVu", "B", 13)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 9, f"Total estimado obra (sin terrenos): {_money(total_obra)} ARS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(
        0,
        4,
        "Documento generado por ARQ-IA. Los importes son estimativos según detección del plano y tabla de precios vigente.",
    )

    return bytes(pdf.output())
