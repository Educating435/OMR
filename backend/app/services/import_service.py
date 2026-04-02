import csv
import io

from app.schemas.exam import AnswerKeyItem, AnswerKeyUpdate


class ImportService:
    def import_answer_keys_csv(self, content: str) -> AnswerKeyUpdate:
        reader = csv.DictReader(io.StringIO(content))
        items = []
        for row in reader:
            items.append(
                AnswerKeyItem(
                    question_no=int(row["question_no"]),
                    correct_option=row["correct_option"].strip().upper(),
                    set_code=row.get("set_code", "A").strip().upper() or "A",
                )
            )
        return AnswerKeyUpdate(items=items)
