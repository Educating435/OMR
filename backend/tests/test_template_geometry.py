from types import SimpleNamespace

from app.services.omr.pdf_generator import CANVAS_HEIGHT_PX, CANVAS_WIDTH_PX, generate_template_geometry, resolve_template_spec


def test_official_template_geometry_for_50_questions() -> None:
    exam = SimpleNamespace(
        id="exam-1",
        title="Mock Test 1",
        subject="Physics",
        total_questions=50,
        options_per_question=4,
        metadata_json={"institute_name": "Alpha Institute", "exam_code": "PHY-001"},
    )

    spec = resolve_template_spec(exam)
    geometry = generate_template_geometry(exam.total_questions, exam.options_per_question, exam=exam)

    assert spec.key == "official_a4_50q_4opt_v1"
    assert geometry["page"]["width_px"] == CANVAS_WIDTH_PX
    assert geometry["page"]["height_px"] == CANVAS_HEIGHT_PX
    assert len(geometry["corner_markers"]) == 4
    assert len(geometry["roll_number_zone"]["columns"]) == 6
    assert len(geometry["set_code_zone"]["bubbles"]) == 4
    assert len(geometry["answer_zone"]["questions"]) == 50
    assert all(len(question["options"]) == 4 for question in geometry["answer_zone"]["questions"])

