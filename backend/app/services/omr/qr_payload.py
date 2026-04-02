import hashlib


def build_qr_payload(template_id: str, exam_id: str, version: int, total_questions: int, options_count: int) -> dict:
    checksum = hashlib.sha256(
        f"{template_id}:{exam_id}:{version}:{total_questions}:{options_count}".encode("utf-8")
    ).hexdigest()[:16]
    return {
        "template_id": template_id,
        "exam_id": exam_id,
        "total_questions": total_questions,
        "options_count": options_count,
        "version": version,
        "checksum": checksum,
    }
