# Android Architecture

Base package: `com.mycompany.omrscanner`

## Layering

- `app`: application bootstrap and activity host only
- `core`: shared enums, utility helpers, UI theme, and network constants
- `domain`: pure models, repository interfaces, and use cases
- `data`: Room/Retrofit implementations and mappers
- `feature_*`: UI state holders and Composables for each feature
- `camera`: capture coordination abstractions
- `omr`: detection, alignment, QR, bubble reading, scoring, and pipeline orchestration
- `sync`: WorkManager background sync

## Rules Enforced

- Composables receive state and callbacks only
- ViewModels call use cases and never contain OpenCV logic
- OMR pipeline depends on OMR submodules, not on Compose
- repository interfaces live in `domain.repository`
- repository implementations live in `data.repository`

## Current Flow

1. `feature_scan.ScanViewModel` requests a capture flow.
2. `domain.usecase.ProcessScanUseCase` delegates to `omr.pipeline.OMRPipeline`.
3. `DefaultOMRPipeline` orchestrates page detection, alignment, QR validation, bubble reading, and scoring.
4. `domain.usecase.SaveScanUseCase` persists via `domain.repository.ScanRepository`.
5. `sync.ScanSyncWorker` uploads pending attempts later.
