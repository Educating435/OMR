# Database Schema

The backend model layer now defines these primary entities:

- `organizations`
- `roles`
- `users`
- `exams`
- `exam_sets`
- `answer_keys`
- `omr_templates`
- `template_versions`
- `students`
- `scan_sessions`
- `scan_images`
- `omr_results`
- `omr_responses`
- `review_flags`
- `exports`
- `audit_logs`

## Compatibility Notes

- The current backend service layer still imports `ExamTemplate` and `ResultAttempt`.
- Those names are preserved as compatibility aliases:
  - `ExamTemplate -> TemplateVersion`
  - `ResultAttempt -> OMRResult`

## Design Direction

- `organizations` provides the tenancy boundary.
- `roles` supports future DB-managed permissions while `users.role` keeps the app’s current enum-based RBAC simple.
- `omr_templates` is the logical template master.
- `template_versions` stores printable/layout-specific revisions.
- `omr_results` stores header-level grading outcomes.
- `omr_responses` stores per-question evaluation detail.
- `review_flags` supports operator/admin review workflows.
- `audit_logs` is the system audit trail for critical actions.
