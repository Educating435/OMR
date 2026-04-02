from dataclasses import asdict, dataclass


@dataclass(slots=True)
class OMRLayout:
    page_size: dict
    markers: dict
    qr_anchor: dict
    roll_number_grid: dict
    set_code_grid: dict
    question_blocks: list[dict]


def build_v1_layout(total_questions: int = 50, options_per_question: int = 4) -> OMRLayout:
    question_blocks: list[dict] = []
    start_x = 70
    start_y = 690
    row_gap = 22
    column_gap = 28

    for question_number in range(1, total_questions + 1):
        block_index = (question_number - 1) // 25
        local_index = (question_number - 1) % 25
        x = start_x + (block_index * 250)
        y = start_y - (local_index * row_gap)
        options = []
        for option_index in range(options_per_question):
            options.append(
                {
                    "option": chr(65 + option_index),
                    "center_x": x + 60 + (option_index * column_gap),
                    "center_y": y,
                    "radius": 8,
                }
            )
        question_blocks.append(
            {
                "question_number": question_number,
                "label_x": x,
                "label_y": y,
                "options": options,
            }
        )

    return OMRLayout(
        page_size={"width": 595, "height": 842, "format": "A4"},
        markers={
            "top_left": {"x": 30, "y": 812, "size": 16},
            "top_right": {"x": 549, "y": 812, "size": 16},
            "bottom_left": {"x": 30, "y": 30, "size": 16},
            "bottom_right": {"x": 549, "y": 30, "size": 16},
        },
        qr_anchor={"x": 455, "y": 735, "size": 100},
        roll_number_grid={"x": 70, "y": 755, "digits": 6, "rows": 10, "bubble_radius": 7, "column_gap": 22, "row_gap": 16},
        set_code_grid={"x": 235, "y": 755, "codes": ["A", "B", "C", "D"], "bubble_radius": 8, "column_gap": 24},
        question_blocks=question_blocks,
    )


def layout_to_dict(layout: OMRLayout) -> dict:
    return asdict(layout)
