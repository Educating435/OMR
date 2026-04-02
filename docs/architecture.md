# Architecture

## Solution Overview

The system is intentionally built around deterministic templates. Every printed sheet is generated from backend-owned geometry:

- page size: A4 portrait
- fixed anchor markers on corners
- QR code containing template identity and revision
- known question count and bubble grid definition
- optional student metadata zones

This design reduces false positives and makes mobile alignment tractable on commodity Android devices.

## Product Modes

- `Super Admin`: manages organization settings, users, exams, templates, analytics, and exports
- `Staff / Scanner Operator`: logs in on Android, downloads exams/templates, scans sheets, reviews flagged scans, syncs results
- `Read-only Viewer`: accesses reports and review dashboards without mutation privileges

## Coordinated Services

1. Android Scanner App
2. Backend API
3. Admin Panel

The current repo uses a single-organization baseline. RBAC is implemented, and multi-organization tenancy can be added by introducing `organization_id` on users, exams, and attempts plus scoped queries.

## OMR Pipeline

1. Android app scans QR and validates template revision.
2. OpenCV detects outer page and anchor markers.
3. Perspective transform normalizes the page to canonical A4 coordinate space.
4. Known bubble ROIs are sampled from template geometry.
5. Darkness ratio and confidence thresholds classify marked bubbles.
6. Result is graded locally against the downloaded answer key.
7. Attempt is stored offline and synced later.

## Security

- JWT access token + refresh token flow
- signed template metadata to prevent mismatched answer keys
- audit trail for answer-key changes and regrading

## Production Readiness Checklist

- add Alembic migrations
- add structured logging and tracing
- add print calibration and skew test dataset
- add RBAC and institute tenancy
- move storage to S3-compatible object storage for scale
