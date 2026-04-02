# OMR Scanner Platform

Strict production-oriented OMR system with this fixed architecture:

`Admin Panel / Android App -> FastAPI on Render -> Hostinger MySQL`

Non-negotiable rules enforced by this repo:

- Android never connects to MySQL directly.
- Business rules live in FastAPI services, not in MySQL.
- Hostinger MySQL is the only server database target.
- OMR detection is classical vision and fixed-template based, not AI-first.

## Final Repository Structure

```text
OMR SCANNER/
|-- admin/
|   |-- src/
|   |   |-- app/
|   |   |-- components/
|   |   |-- features/
|   |   |   |-- auth/
|   |   |   |-- dashboard/
|   |   |   |-- exams/
|   |   |   |-- answerKeys/
|   |   |   |-- templates/
|   |   |   |-- results/
|   |   |   |-- review/
|   |   |   `-- users/
|   |   `-- lib/
|   `-- package.json
|-- android/
|   |-- app/
|   |   `-- src/main/java/com/mycompany/omrscanner/
|   |       |-- app/
|   |       |-- auth/
|   |       |-- exam/
|   |       |-- scanner/
|   |       |-- result/
|   |       |-- history/
|   |       |-- settings/
|   |       |-- camera/
|   |       |-- omr/
|   |       |   |-- detection/
|   |       |   |-- alignment/
|   |       |   |-- template/
|   |       |   |-- bubble/
|   |       |   |-- scoring/
|   |       |   `-- pipeline/
|   |       |-- sync/
|   |       |-- data/
|   |       |   |-- local/
|   |       |   |-- remote/
|   |       |   `-- repository/
|   |       |-- domain/
|   |       |   |-- repository/
|   |       |   |-- usecase/
|   |       |   `-- usecases/
|   |       `-- di/
|   `-- settings.gradle.kts
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |-- database/
|   |   |-- models/
|   |   |-- modules/
|   |   |   |-- auth/
|   |   |   |-- users/
|   |   |   |-- exams/
|   |   |   |-- answer_keys/
|   |   |   |-- templates/
|   |   |   |-- pdf_generation/
|   |   |   |-- results/
|   |   |   |-- exports/
|   |   |   `-- audit_logs/
|   |   |-- security/
|   |   `-- storage/
|   |-- migrations/
|   |   `-- versions/
|   |-- Dockerfile
|   |-- start.sh
|   `-- requirements.txt
|-- docs/
|-- docker-compose.yml
`-- README.md
```

## Implementation Status

### Backend

- IMPLEMENTED: FastAPI entrypoint, API router, MySQL-first settings, SQLAlchemy models, JWT login flow, storage abstraction, audit logging.
- IMPLEMENTED: exam APIs, answer key replacement API, A4 template generation API, result sync API, result review API, CSV export API.
- IMPLEMENTED: Alembic baseline migration for Hostinger MySQL deployment.
- TODO NEXT: richer validation, pagination, file download endpoint for generated PDFs, stronger role permissions, automated tests aligned to new modules.

### Admin Panel

- IMPLEMENTED: React + Vite + TypeScript + Tailwind shell.
- IMPLEMENTED: login, dashboard, exam creation, answer key upload shell, template generation, results list, review queue, user creation.
- TODO NEXT: form validation, toast/error handling polish, real answer-key CSV import, PDF download and preview.

### Android App

- IMPLEMENTED: Kotlin + Compose + Hilt app shell with the requested package boundaries.
- IMPLEMENTED: Room cache entities, Retrofit API layer, repository contracts, WorkManager sync worker shell.
- IMPLEMENTED: controlled-template OMR pipeline shell for detection, alignment, bubble interpretation, and scoring separation.
- PARTIAL: UI modules are scaffolded and architecture-safe, but not yet fully wired to repository-backed state.
- TODO NEXT: CameraX preview/capture, OpenCV page detection and perspective correction, QR read, roll-number bubble decoding, conflict-safe sync retries.

## Backend Local Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Required `.env` values:

- `DATABASE_URL=mysql+pymysql://...`
- `JWT_SECRET_KEY=...`
- `STORAGE_ROOT=storage`

## Admin Local Setup

```bash
cd admin
npm install
npm run dev
```

Optional env:

- `VITE_API_BASE_URL=http://localhost:8000/api/v1`

## Android Local Setup

1. Open `/android` in Android Studio.
2. Use the `app` run configuration.
3. Point the emulator/device to the FastAPI host.
4. Keep backend access through Retrofit only.

## Render Deployment

Backend service settings:

- Runtime: Docker
- Root directory: `backend`
- Start command: use bundled `start.sh`
- Health check path: `/api/v1/health`

Environment variables on Render:

- `DATABASE_URL=mysql+pymysql://HOSTINGER_USER:HOSTINGER_PASSWORD@HOSTINGER_HOST:3306/HOSTINGER_DB`
- `JWT_SECRET_KEY=strong-production-secret`
- `STORAGE_ROOT=/app/storage`
- `CORS_ORIGINS=https://your-admin-domain`

## Hostinger MySQL Configuration

Use Hostinger MySQL as the only server database for:

- users
- exams
- answer keys
- template metadata
- results
- responses
- audit logs

Do not:

- connect Android directly to MySQL
- move grading logic into SQL procedures
- replace Hostinger MySQL with a Render-managed database

## OMR v1 Scope

- Controlled-template OMR only
- One official A4 template format
- Four corner markers mandatory
- QR code mandatory
- 50 questions
- 4 options per question
- 6-digit roll number
- set codes `A/B/C/D`
