from dataclasses import dataclass


@dataclass
class GradeResult:
    score: float
    max_score: float
    correct: int
    incorrect: int
    blank: int


def grade_responses(
    answer_key: dict[str, str],
    responses: dict[str, str | None],
    positive_marks: int,
    negative_marks: int,
) -> GradeResult:
    correct = 0
    incorrect = 0
    blank = 0

    for question, expected in answer_key.items():
        actual = responses.get(question)
        if not actual:
            blank += 1
        elif actual == expected:
            correct += 1
        else:
            incorrect += 1

    score = (correct * positive_marks) - (incorrect * negative_marks)
    max_score = len(answer_key) * positive_marks
    return GradeResult(score=score, max_score=max_score, correct=correct, incorrect=incorrect, blank=blank)

