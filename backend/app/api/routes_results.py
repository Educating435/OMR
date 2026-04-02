from fastapi import APIRouter, Depends

from app.api.deps import DBSession, get_current_user, get_pagination, require_roles
from app.models import User, UserRole
from app.repositories.exam_repository import ExamRepository
from app.repositories.result_repository import ResultRepository
from app.schemas.result import AnalyticsSnapshot, BulkSyncRequest, MessageResponse, ResultRead, ResultReviewUpdate, ScanSubmission
from app.services.result_service import ResultService


router = APIRouter(prefix="/results")


@router.post("", response_model=ResultRead)
def submit_result(
    payload: ScanSubmission,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.STAFF)),
) -> ResultRead:
    del current_user
    service = ResultService(ExamRepository(db), ResultRepository(db))
    return ResultRead.model_validate(service.submit_scan(payload))


@router.get("")
def list_results(
    db: DBSession,
    pagination=Depends(get_pagination),
    current_user: User = Depends(get_current_user),
) -> dict:
    del current_user
    service = ResultService(ExamRepository(db), ResultRepository(db))
    items, meta = service.list_all_results(pagination.page, pagination.page_size)
    return {"items": [ResultRead.model_validate(item).model_dump() for item in items], "meta": meta.model_dump()}


@router.get("/{result_id}", response_model=ResultRead)
def get_result(
    result_id: str,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ResultRead:
    del current_user
    return ResultRead.model_validate(ResultService(ExamRepository(db), ResultRepository(db)).get_result(result_id))


@router.post("/{result_id}/review", response_model=ResultRead)
def review_result(
    result_id: str,
    db: DBSession,
    payload: ResultReviewUpdate,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.STAFF)),
) -> ResultRead:
    service = ResultService(ExamRepository(db), ResultRepository(db))
    return ResultRead.model_validate(service.review_result(result_id, payload, reviewer_id=current_user.id))


@router.post("/bulk-sync", response_model=list[ResultRead])
def bulk_sync(
    payload: BulkSyncRequest,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.STAFF)),
) -> list[ResultRead]:
    del current_user
    service = ResultService(ExamRepository(db), ResultRepository(db))
    return [ResultRead.model_validate(service.submit_scan(item)) for item in payload.items]


@router.get("/analytics/summary", response_model=AnalyticsSnapshot)
def analytics_summary(
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> AnalyticsSnapshot:
    del current_user
    return ResultService(ExamRepository(db), ResultRepository(db)).analytics()
