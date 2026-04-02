# OMR Template Generator

## Official Template

The first official machine-generated template is:

- A4 portrait
- 300 DPI internal coordinate space
- `2480 x 3508` deterministic layout canvas
- 50 questions
- 4 options per question (`A/B/C/D`)
- 6-digit roll number bubble zone
- 4 set codes (`A/B/C/D`)

## Mandatory Elements

- institute name
- exam title
- exam code
- template version
- QR code
- 4 corner alignment markers
- roll number bubble area
- set code bubble area
- answer area
- optional text fields for name, class, and date

## QR Payload

The QR payload is deterministic and includes:

- `template_id`
- `exam_id`
- `total_questions`
- `options_count`
- `version`

## Layout Metadata

The backend stores machine-readable metadata in the template version record:

- page size and DPI
- corner marker spec
- roll number bubble coordinates
- set code bubble coordinates
- answer bubble coordinates
- scale profiles for 50, 100, and 180 question families

## Scaling Strategy

- `50 questions`: 2 answer columns
- `100 questions`: 2 denser answer columns
- `180 questions`: 3 answer columns

Bubble positions are generated mathematically from spacing constants and per-layout profiles rather than hand-placed coordinates.
