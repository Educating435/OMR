# Mobile Scanning Pipeline

## Capture Strategy

The Android app should guide the operator into a predictable capture:

- full A4 page visible
- high-contrast corner anchors inside frame guides
- minimum focus and exposure checks before analysis
- QR readable before final capture acceptance

## Processing Stages

1. Convert CameraX frame to grayscale OpenCV `Mat`.
2. Run adaptive thresholding to stabilize against lighting variation.
3. Detect page contour and perform perspective correction to canonical template size.
4. Detect anchor markers and reject frames whose geometry does not match expected tolerances.
5. Decode QR payload and validate `exam_id`, `revision`, and checksum.
6. Sample known bubble regions from template geometry.
7. Compute fill ratio and confidence score for each bubble.
8. Resolve single-mark, multi-mark, and blank answers using thresholds.
9. Grade locally and persist to Room.
10. Queue sync through WorkManager.

## Failure Handling

- if QR fails: request reframe before capture
- if anchors mismatch: reject as wrong template or warped sheet
- if bubble confidence is low: mark question as uncertain and surface manual review
- if sync fails: keep attempt offline and retry automatically
