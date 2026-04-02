from __future__ import annotations

import json
from dataclasses import dataclass
from math import ceil
from pathlib import Path

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from app.models import Exam


A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297
CANVAS_WIDTH_PX = 2480
CANVAS_HEIGHT_PX = 3508
PX_PER_MM = CANVAS_WIDTH_PX / A4_WIDTH_MM
PT_PER_MM = mm


def mm_to_px(value_mm: float) -> int:
    return round(value_mm * PX_PER_MM)


def px_to_pt(value_px: float) -> float:
    return (value_px / PX_PER_MM) * PT_PER_MM


def y_px_to_pt_from_top(y_px: float) -> float:
    return A4[1] - px_to_pt(y_px)


@dataclass(frozen=True)
class OfficialTemplateSpec:
    key: str
    questions: int
    options_count: int
    roll_digits: int
    set_codes: list[str]
    answer_columns: int
    institute_name: str


OFFICIAL_TEMPLATE_50 = OfficialTemplateSpec(
    key="official_a4_50q_4opt_v1",
    questions=50,
    options_count=4,
    roll_digits=6,
    set_codes=["A", "B", "C", "D"],
    answer_columns=2,
    institute_name="Institute Name",
)


def resolve_template_spec(exam: Exam) -> OfficialTemplateSpec:
    metadata = exam.metadata_json or {}
    total_questions = exam.total_questions
    options_count = exam.options_per_question
    answer_columns = 2 if total_questions <= 100 else 3

    if total_questions == 50 and options_count == 4:
        return OFFICIAL_TEMPLATE_50

    return OfficialTemplateSpec(
        key=f"a4_{total_questions}q_{options_count}opt_v1",
        questions=total_questions,
        options_count=options_count,
        roll_digits=int(metadata.get("roll_digits", 6)),
        set_codes=list(metadata.get("set_codes", ["A", "B", "C", "D"])),
        answer_columns=answer_columns,
        institute_name=str(metadata.get("institute_name", "Institute Name")),
    )


def _corner_markers() -> list[dict]:
    marker_size_mm = 8
    padding_mm = 10
    positions = [
        ("top_left", padding_mm, padding_mm),
        ("top_right", A4_WIDTH_MM - padding_mm - marker_size_mm, padding_mm),
        ("bottom_left", padding_mm, A4_HEIGHT_MM - padding_mm - marker_size_mm),
        ("bottom_right", A4_WIDTH_MM - padding_mm - marker_size_mm, A4_HEIGHT_MM - padding_mm - marker_size_mm),
    ]
    return [
        {
            "name": name,
            "x_px": mm_to_px(x_mm),
            "y_px": mm_to_px(y_mm),
            "size_px": mm_to_px(marker_size_mm),
        }
        for name, x_mm, y_mm in positions
    ]


def _build_roll_number_zone(spec: OfficialTemplateSpec) -> dict:
    start_x = mm_to_px(110)
    start_y = mm_to_px(205)
    col_gap = mm_to_px(7.2)
    row_gap = mm_to_px(6.0)
    bubble_diameter = mm_to_px(3.8)
    columns = []
    for digit_index in range(spec.roll_digits):
        bubbles = []
        for value in range(10):
            bubbles.append(
                {
                    "digit": digit_index + 1,
                    "value": str(value),
                    "cx_px": start_x + digit_index * col_gap,
                    "cy_px": start_y + value * row_gap,
                    "diameter_px": bubble_diameter,
                }
            )
        columns.append({"digit_index": digit_index + 1, "bubbles": bubbles})
    return {
        "label": "Roll Number",
        "start_x_px": start_x,
        "start_y_px": start_y,
        "columns": columns,
    }


def _build_set_code_zone(spec: OfficialTemplateSpec) -> dict:
    start_x = mm_to_px(165)
    start_y = mm_to_px(205)
    row_gap = mm_to_px(8)
    bubble_diameter = mm_to_px(4.2)
    return {
        "label": "Set Code",
        "bubbles": [
            {
                "code": code,
                "cx_px": start_x,
                "cy_px": start_y + idx * row_gap,
                "diameter_px": bubble_diameter,
            }
            for idx, code in enumerate(spec.set_codes)
        ],
    }


def _build_answer_zone(spec: OfficialTemplateSpec) -> dict:
    top_y = mm_to_px(90)
    left_margin = mm_to_px(24)
    usable_width = CANVAS_WIDTH_PX - mm_to_px(48)
    column_gap = mm_to_px(8)
    option_gap = mm_to_px(7.5)
    row_gap = mm_to_px(8)
    question_number_width = mm_to_px(12)
    bubble_diameter = mm_to_px(4)
    rows_per_column = ceil(spec.questions / spec.answer_columns)
    column_width = (usable_width - ((spec.answer_columns - 1) * column_gap)) / spec.answer_columns

    questions = []
    for question_no in range(1, spec.questions + 1):
        column_index = (question_no - 1) // rows_per_column
        row_index = (question_no - 1) % rows_per_column
        base_x = left_margin + round(column_index * (column_width + column_gap))
        base_y = top_y + row_index * row_gap
        option_bubbles = []
        for option_index in range(spec.options_count):
            option_bubbles.append(
                {
                    "option": chr(65 + option_index),
                    "cx_px": base_x + question_number_width + option_index * option_gap,
                    "cy_px": base_y,
                    "diameter_px": bubble_diameter,
                }
            )
        questions.append(
            {
                "question_no": question_no,
                "column_index": column_index + 1,
                "row_index": row_index + 1,
                "label_x_px": base_x,
                "label_y_px": base_y,
                "options": option_bubbles,
            }
        )
    return {
        "columns": spec.answer_columns,
        "rows_per_column": rows_per_column,
        "questions": questions,
    }


def generate_template_geometry(total_questions: int, options_per_question: int, exam: Exam | None = None) -> dict:
    if exam is not None:
        spec = resolve_template_spec(exam)
    else:
        spec = OfficialTemplateSpec(
            key=f"a4_{total_questions}q_{options_per_question}opt_v1",
            questions=total_questions,
            options_count=options_per_question,
            roll_digits=6,
            set_codes=["A", "B", "C", "D"],
            answer_columns=2 if total_questions <= 100 else 3,
            institute_name="Institute Name",
        )

    metadata = exam.metadata_json if exam is not None and exam.metadata_json else {}
    header_zone = {
        "institute_name": str(metadata.get("institute_name", spec.institute_name)),
        "exam_title": exam.title if exam is not None else "Exam Title",
        "exam_code": str(metadata.get("exam_code", (exam.id[:8] if exam is not None else "EXAMCODE"))),
        "template_version": int(metadata.get("template_version", 1)),
        "optional_fields": ["name", "class", "date"],
    }

    return {
        "page": {
            "width_mm": A4_WIDTH_MM,
            "height_mm": A4_HEIGHT_MM,
            "width_px": CANVAS_WIDTH_PX,
            "height_px": CANVAS_HEIGHT_PX,
            "dpi": 300,
            "orientation": "portrait",
        },
        "template_family": spec.key,
        "header": header_zone,
        "corner_markers": _corner_markers(),
        "marker_spec_json": {
            "type": "square_fiducials",
            "count": 4,
            "contrast": "high",
            "expected_positions": _corner_markers(),
        },
        "roll_number_zone": _build_roll_number_zone(spec),
        "set_code_zone": _build_set_code_zone(spec),
        "answer_zone": _build_answer_zone(spec),
        "machine_readable_zones": {
            "roll_number": {"digits": spec.roll_digits},
            "set_code": {"codes": spec.set_codes},
            "answers": {"questions": spec.questions, "options_count": spec.options_count},
        },
        "scaling_profiles": [
            {"questions": 50, "options_count": 4, "columns": 2},
            {"questions": 100, "options_count": 4, "columns": 2},
            {"questions": 180, "options_count": 4, "columns": 3},
        ],
    }


def render_exam_template_pdf(exam: Exam, qr_payload: dict, geometry: dict, file_path: Path) -> None:
    qr_image = qrcode.make(json.dumps(qr_payload, separators=(",", ":"), sort_keys=True))
    pdf = canvas.Canvas(str(file_path), pagesize=A4)
    width_pt, _ = A4

    header = geometry["header"]
    pdf.setTitle(f"{exam.title} OMR Sheet")
    pdf.setLineWidth(1)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(px_to_pt(mm_to_px(18)), y_px_to_pt_from_top(mm_to_px(18)), header["institute_name"])
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(px_to_pt(mm_to_px(18)), y_px_to_pt_from_top(mm_to_px(28)), header["exam_title"])
    pdf.setFont("Helvetica", 9)
    pdf.drawString(px_to_pt(mm_to_px(18)), y_px_to_pt_from_top(mm_to_px(36)), f"Exam Code: {header['exam_code']}")
    pdf.drawString(px_to_pt(mm_to_px(18)), y_px_to_pt_from_top(mm_to_px(42)), f"Template Version: {qr_payload['version']}")
    pdf.drawString(px_to_pt(mm_to_px(18)), y_px_to_pt_from_top(mm_to_px(48)), f"Questions: {qr_payload['total_questions']}")

    field_y_positions_mm = [60, 67, 74]
    labels = ["Name", "Class", "Date"]
    for label, y_mm in zip(labels, field_y_positions_mm, strict=True):
        y_pt = y_px_to_pt_from_top(mm_to_px(y_mm))
        x_pt = px_to_pt(mm_to_px(18))
        pdf.drawString(x_pt, y_pt, f"{label}:")
        pdf.line(x_pt + px_to_pt(mm_to_px(18)), y_pt - 2, x_pt + px_to_pt(mm_to_px(80)), y_pt - 2)

    qr_size_px = mm_to_px(24)
    pdf.drawInlineImage(
        qr_image,
        width_pt - px_to_pt(mm_to_px(34)),
        y_px_to_pt_from_top(mm_to_px(34)),
        px_to_pt(qr_size_px),
        px_to_pt(qr_size_px),
    )

    for marker in geometry["corner_markers"]:
        x = px_to_pt(marker["x_px"])
        y = y_px_to_pt_from_top(marker["y_px"] + marker["size_px"])
        size = px_to_pt(marker["size_px"])
        pdf.setFillGray(0)
        pdf.rect(x, y, size, size, stroke=1, fill=1)
        inner = size * 0.35
        pdf.setFillGray(1)
        pdf.rect(x + (size - inner) / 2, y + (size - inner) / 2, inner, inner, stroke=0, fill=1)
        pdf.setFillGray(0)

    roll_zone = geometry["roll_number_zone"]
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(px_to_pt(roll_zone["start_x_px"]), y_px_to_pt_from_top(roll_zone["start_y_px"] - mm_to_px(6)), roll_zone["label"])
    pdf.setFont("Helvetica", 7)
    for column in roll_zone["columns"]:
        for bubble in column["bubbles"]:
            x = px_to_pt(bubble["cx_px"])
            y = y_px_to_pt_from_top(bubble["cy_px"])
            r = px_to_pt(bubble["diameter_px"] / 2)
            pdf.circle(x, y, r)
            pdf.drawCentredString(x, y + px_to_pt(mm_to_px(2.3)), bubble["value"])

    set_zone = geometry["set_code_zone"]
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(px_to_pt(set_zone["bubbles"][0]["cx_px"] - mm_to_px(8)), y_px_to_pt_from_top(set_zone["bubbles"][0]["cy_px"] - mm_to_px(6)), set_zone["label"])
    pdf.setFont("Helvetica", 8)
    for bubble in set_zone["bubbles"]:
        x = px_to_pt(bubble["cx_px"])
        y = y_px_to_pt_from_top(bubble["cy_px"])
        r = px_to_pt(bubble["diameter_px"] / 2)
        pdf.circle(x, y, r)
        pdf.drawString(x + px_to_pt(mm_to_px(4)), y - 2, bubble["code"])

    answer_zone = geometry["answer_zone"]
    pdf.setFont("Helvetica", 7)
    for question in answer_zone["questions"]:
        pdf.drawString(
            px_to_pt(question["label_x_px"]),
            y_px_to_pt_from_top(question["label_y_px"]) - 2,
            f"{question['question_no']:02d}",
        )
        for option in question["options"]:
            x = px_to_pt(option["cx_px"])
            y = y_px_to_pt_from_top(option["cy_px"])
            r = px_to_pt(option["diameter_px"] / 2)
            pdf.circle(x, y, r)
            pdf.drawCentredString(x, y + px_to_pt(mm_to_px(2.6)), option["option"])

    pdf.showPage()
    pdf.save()
