from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps import DBSession, get_current_user, get_pagination, require_roles
from app.models import User, UserRole
from app.repositories.audit_repository import AuditRepository
from app.repositories.exam_repository import ExamRepository
from app.schemas.exam import AnswerKeyItem, AnswerKeyUpdate, ExamCreate, ExamRead, ExamUpdate
from app.services.exam_service import ExamService
from app.services.import_service import ImportService


router = APIRouter(prefix="/exams")


@router.get("")
def list_exams(
    db: DBSession,
    pagination=Depends(get_pagination),
    current_user: User = Depends(get_current_user),
) -> dict:
    del current_user
    items, meta = ExamService(ExamRepository(db)).list_exams(pagination.page, pagination.page_size)
    return {"items": [ExamRead.model_validate(item).model_dump() for item in items], "meta": meta.model_dump()}


@router.post("", response_model=ExamRead, status_code=status.HTTP_201_CREATED)
def create_exam(
    payload: ExamCreate,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> ExamRead:
    exam = ExamService(ExamRepository(db), AuditRepository(db)).create_exam(payload, owner_id=current_user.id)
    return ExamRead.model_validate(exam)


@router.get("/{exam_id}", response_model=ExamRead)
def get_exam(exam_id: str, db: DBSession, current_user: User = Depends(get_current_user)) -> ExamRead:
    del current_user
    exam = ExamService(ExamRepository(db)).get_exam(exam_id)
    if exam is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return ExamRead.model_validate(exam)


@router.put("/{exam_id}", response_model=ExamRead)
def update_exam(
    exam_id: str,
    payload: ExamUpdate,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> ExamRead:
    exam = ExamService(ExamRepository(db), AuditRepository(db)).update_exam(exam_id, payload, actor_user_id=current_user.id)
    return ExamRead.model_validate(exam)


@router.delete("/{exam_id}", response_model=dict)
def delete_exam(
    exam_id: str,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> dict:
    ExamService(ExamRepository(db), AuditRepository(db)).delete_exam(exam_id, actor_user_id=current_user.id)
    return {"message": "Exam deleted"}


@router.get("/{exam_id}/answer-keys", response_model=list[AnswerKeyItem])
def get_answer_keys(
    exam_id: str,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> list[AnswerKeyItem]:
    del current_user
    items = ExamService(ExamRepository(db), AuditRepository(db)).get_answer_keys(exam_id)
    return [AnswerKeyItem(question_no=item.question_no, correct_option=item.correct_option, set_code=item.set_code) for item in items]


@router.put("/{exam_id}/answer-keys", response_model=list[AnswerKeyItem])
def replace_answer_keys(
    exam_id: str,
    payload: AnswerKeyUpdate,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> list[AnswerKeyItem]:
    items = ExamService(ExamRepository(db), AuditRepository(db)).replace_answer_keys(exam_id, payload, actor_user_id=current_user.id)
    return [AnswerKeyItem(question_no=item.question_no, correct_option=item.correct_option, set_code=item.set_code) for item in items]


@router.post("/{exam_id}/answer-keys/import-csv", response_model=list[AnswerKeyItem])
async def import_answer_keys_csv(
    exam_id: str,
    db: DBSession,
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> list[AnswerKeyItem]:
    content = (await file.read()).decode("utf-8")
    payload = ImportService().import_answer_keys_csv(content)
    items = ExamService(ExamRepository(db), AuditRepository(db)).replace_answer_keys(exam_id, payload, actor_user_id=current_user.id)
    return [AnswerKeyItem(question_no=item.question_no, correct_option=item.correct_option, set_code=item.set_code) for item in items]
