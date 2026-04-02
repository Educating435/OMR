import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.modules.results.service import ResultService
from app.storage.local import LocalStorageProvider


class ExportService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.storage = LocalStorageProvider()

    def export_results_csv(self, exam_id: str | None = None) -> str:
        results = ResultService(self.db).list_results(exam_id=exam_id)
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["result_id", "exam_id", "roll_number", "set_code", "score", "max_score", "needs_review", "created_at"])
        for result in results:
            writer.writerow(
                [
                    result.id,
                    result.exam_id,
                    result.roll_number,
                    result.set_code,
                    result.score,
                    result.max_score,
                    result.needs_review,
                    result.created_at.isoformat(),
                ]
            )
        return self.storage.save_bytes("exports/results.csv", buffer.getvalue().encode("utf-8"))
