from app.services.omr.grading import grade_responses


def test_grade_responses_counts_correct_incorrect_and_blank() -> None:
    result = grade_responses(
        answer_key={"1": "A", "2": "B", "3": "C"},
        responses={"1": "A", "2": "D", "3": None},
        positive_marks=4,
        negative_marks=1,
    )

    assert result.correct == 1
    assert result.incorrect == 1
    assert result.blank == 1
    assert result.score == 3
    assert result.max_score == 12

