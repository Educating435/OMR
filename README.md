# OMR Scanner Platform

Production-oriented controlled-template OMR platform with:

- Native Android app for capture, grading, offline storage, and sync
- FastAPI backend for auth, exams, templates, scans, and results
- React admin panel for institute operations
- PDF OMR template generation with QR-backed metadata

## Monorepo Layout

- `backend/` FastAPI + SQLAlchemy + PostgreSQL-ready API
- `admin/` React + Vite + TypeScript admin panel
- `android/` Kotlin + Compose Android application
- `docs/` architecture and OMR pipeline notes

## Roles

- `super_admin`: manage users, exams, templates, analytics, and exports
- `staff`: fetch exams/templates, scan sheets, review flagged scans, sync results
- `viewer`: read-only access to reports and flagged-scan visibility

## Coordinated Apps

1. Android Scanner App: offline capture, on-device grading, local storage, deferred sync
2. Backend API: auth, exam/template lifecycle, PDF generation, review workflow, analytics, export
3. Admin Panel: operations console for exams, templates, flagged scans, users, and reports

## Product Model

This project implements a controlled-template OMR workflow, not arbitrary sheet recognition:

1. Admin creates an exam and answer key.
2. Backend generates an OMR template PDF with deterministic markers and QR metadata.
3. Institute prints the A4 sheet.
4. Student fills the sheet.
5. Android app scans the sheet using a guided CameraX pipeline.
6. The app aligns the page against the known template, computes answers, grades locally, and stores the attempt.
7. WorkManager syncs the result to the backend when network is available.

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Admin

```bash
cd admin
npm install
npm run dev
```

### Android

Open `android/` in Android Studio and run the `app` configuration.
