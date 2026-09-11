from __future__ import annotations

from pathlib import Path
import re
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile, status

from app.schemas.upvc_onboarding import (
    OnboardingInitialize,
    OnboardingRead,
    RuleAction,
)
from app.utils.tenant import get_tenant_id
from app.verticals.upvc.onboarding import BusinessDocument
from app.verticals.upvc.onboarding_schema import DOCUMENT_TYPES
from app.verticals.upvc.onboarding_service import UPVCOnboardingService

router = APIRouter(prefix="/upvc/onboarding", tags=["upvc-onboarding"])
service = UPVCOnboardingService()
UPLOAD_ROOT = Path("backend/.data/upvc-onboarding")
MAX_DOCUMENT_BYTES = 25 * 1024 * 1024
_SAFE_TENANT = re.compile(r"[^A-Za-z0-9_.-]")


def _storage_tenant_id(tenant_id: str) -> str:
    sanitized = _SAFE_TENANT.sub("_", tenant_id).strip("._")
    if not sanitized:
        raise HTTPException(status_code=400, detail="Invalid tenant identifier.")
    return sanitized


def _serialize(tenant_id: str) -> OnboardingRead:
    config = service.configuration(tenant_id)
    return OnboardingRead(
        tenant_id=config.tenant_id,
        company_name=config.company_name,
        documents=[
            {
                "id": doc.id,
                "name": doc.name,
                "document_type": doc.document_type,
                "source_uri": doc.source_uri,
            }
            for doc in config.documents
        ],
        rules=[
            {
                "key": rule.key,
                "value": rule.value,
                "source": rule.source,
                "confidence": float(rule.confidence),
                "status": rule.status,
                "source_document_id": rule.source_document_id,
            }
            for rule in config.rules.values()
        ],
        readiness=service.readiness(config),
    )


@router.get("", response_model=OnboardingRead)
async def get_onboarding(request: Request) -> OnboardingRead:
    return _serialize(get_tenant_id(request))


@router.post("", response_model=OnboardingRead, status_code=status.HTTP_201_CREATED)
async def initialize_onboarding(payload: OnboardingInitialize, request: Request) -> OnboardingRead:
    tenant_id = get_tenant_id(request)
    service.set_company_name(tenant_id, payload.company_name)
    return _serialize(tenant_id)


@router.post("/documents", response_model=OnboardingRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    document_type: str = Form("other"),
) -> OnboardingRead:
    tenant_id = get_tenant_id(request)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Document filename is required.")
    if document_type not in DOCUMENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported document_type: {document_type}")

    content = await file.read(MAX_DOCUMENT_BYTES + 1)
    if len(content) > MAX_DOCUMENT_BYTES:
        raise HTTPException(status_code=413, detail="Document exceeds the 25 MB limit.")

    tenant_dir = UPLOAD_ROOT / _storage_tenant_id(tenant_id)
    tenant_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename).name
    stored_name = f"{uuid4().hex}_{safe_name}"
    destination = tenant_dir / stored_name
    destination.write_bytes(content)

    document = BusinessDocument(
        name=safe_name,
        document_type=document_type,
        source_uri=str(destination),
    )
    service.add_document(tenant_id, document, content)
    return _serialize(tenant_id)


@router.post("/rules/{key:path}/review", response_model=OnboardingRead)
async def review_rule(key: str, payload: RuleAction, request: Request) -> OnboardingRead:
    tenant_id = get_tenant_id(request)
    try:
        if payload.action == "verify":
            service.verify_rule(tenant_id, key)
        else:
            service.reject_rule(tenant_id, key)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _serialize(tenant_id)
