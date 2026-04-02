from io import BytesIO
import json

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.modules.pdf_generation.omr_layout import build_v1_layout, layout_to_dict


class OMRPdfService:
    def build_template_document(self, exam_id: str, template_code: str, total_questions: int) -> tuple[bytes, dict]:
        layout = build_v1_layout(total_questions=total_questions)
        layout_dict = layout_to_dict(layout)
        qr_payload = {"exam_id": exam_id, "template_code": template_code, "template_version": 1}

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setTitle(f"OMR Template {template_code}")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 800, "Controlled OMR Sheet")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 785, f"Template: {template_code}")
        pdf.drawString(50, 771, "Version: 1")
        pdf.drawString(50, 757, "Questions: 50 | Roll Number: 6 digits | Set Code: A/B/C/D")

        for marker in layout_dict["markers"].values():
            pdf.rect(marker["x"], marker["y"], marker["size"], marker["size"], stroke=1, fill=1)

        qr_image = qrcode.make(json.dumps(qr_payload))
        qr_buffer = BytesIO()
        qr_image.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr = ImageReader(qr_buffer)
        qr_anchor = layout_dict["qr_anchor"]
        pdf.drawImage(qr, qr_anchor["x"], qr_anchor["y"], qr_anchor["size"], qr_anchor["size"])

        self._draw_roll_number(pdf, layout_dict["roll_number_grid"])
        self._draw_set_code(pdf, layout_dict["set_code_grid"])
        self._draw_questions(pdf, layout_dict["question_blocks"])

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return buffer.read(), {"qr_payload": qr_payload, "layout": layout_dict}

    def _draw_roll_number(self, pdf: canvas.Canvas, grid: dict) -> None:
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(grid["x"], grid["y"] + 26, "Roll Number")
        pdf.setFont("Helvetica", 8)
        for digit_index in range(grid["digits"]):
            x = grid["x"] + (digit_index * grid["column_gap"])
            pdf.drawString(x + 2, grid["y"] + 12, str(digit_index + 1))
            for row in range(grid["rows"]):
                y = grid["y"] - (row * grid["row_gap"])
                pdf.circle(x, y, grid["bubble_radius"])
                pdf.drawString(x + 10, y - 3, str(row))

    def _draw_set_code(self, pdf: canvas.Canvas, grid: dict) -> None:
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(grid["x"], grid["y"] + 26, "Set Code")
        pdf.setFont("Helvetica", 8)
        for index, code in enumerate(grid["codes"]):
            x = grid["x"] + (index * grid["column_gap"])
            pdf.circle(x, grid["y"], grid["bubble_radius"])
            pdf.drawString(x - 3, grid["y"] + 12, code)

    def _draw_questions(self, pdf: canvas.Canvas, question_blocks: list[dict]) -> None:
        pdf.setFont("Helvetica", 8)
        for block in question_blocks:
            pdf.drawString(block["label_x"], block["label_y"] - 3, f"{block['question_number']:02d}")
            for option in block["options"]:
                pdf.circle(option["center_x"], option["center_y"], option["radius"])
                pdf.drawString(option["center_x"] - 2, option["center_y"] + 12, option["option"])
