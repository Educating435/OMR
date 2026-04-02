from app.repositories.exam_repository import ExamRepository
from app.schemas.result import ResultExportRow


class ExportService:
    def __init__(self, repository: ExamRepository) -> None:
        self.repository = repository

    def export_results(self, exam_id: str) -> list[ResultExportRow]:
        attempts = self.repository.list_results(exam_id, offset=0, limit=10_000)
        return [
            ResultExportRow(
                student_identifier=item.student_identifier,
                score=item.score,
                max_score=item.max_score,
                percentage=0 if item.max_score == 0 else round((item.score / item.max_score) * 100, 2),
            )
            for item in attempts
        ]
