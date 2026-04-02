class ExportWorker:
    """Placeholder for future async export jobs via Celery/RQ/Arq."""

    def enqueue_exam_export(self, exam_id: str) -> dict[str, str]:
        return {"status": "queued", "exam_id": exam_id}
