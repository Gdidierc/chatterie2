from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import or_
from sqlmodel import Session, select

from .database import get_session, init_db
from .models import Cat, DocumentAttachment, Kitten, Litter
from .routers import cats, compliance, leads, litters

app = FastAPI(title="ChatterieSync", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cats.router)
app.include_router(litters.router)
app.include_router(leads.router)
app.include_router(compliance.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/exports/cat/{cat_id}")
def export_cat(cat_id: int, session: Session = Depends(get_session)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Chat introuvable")

    attachments = session.exec(
        select(DocumentAttachment).where(DocumentAttachment.cat_id == cat_id)
    ).all()
    kittens = session.exec(select(Kitten).where(or_(Kitten.sire_id == cat_id, Kitten.dam_id == cat_id))).all()

    export_dir = Path("data/exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    export_path = export_dir / f"cat_{cat_id}_{timestamp}.zip"

    with ZipFile(export_path, "w") as zf:
        # metadata json
        import json

        metadata: dict[str, Any] = {
            "cat": cat.dict(),
            "kittens": [kitten.dict() for kitten in kittens],
            "attachments": [attachment.dict() for attachment in attachments],
        }
        zf.writestr("metadata.json", json.dumps(metadata, default=str, indent=2))
        for attachment in attachments:
            path = Path(attachment.file_path)
            if path.exists():
                zf.write(path, arcname=path.name)

    return FileResponse(export_path)


@app.get("/exports/litter/{litter_id}")
def export_litter(litter_id: int, session: Session = Depends(get_session)):
    litter = session.get(Litter, litter_id)
    if not litter:
        raise HTTPException(status_code=404, detail="Portée introuvable")

    kittens = session.exec(select(Kitten).where(Kitten.litter_id == litter_id)).all()
    attachments = session.exec(
        select(DocumentAttachment).where(DocumentAttachment.litter_id == litter_id)
    ).all()

    export_dir = Path("data/exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    export_path = export_dir / f"litter_{litter_id}_{timestamp}.zip"

    with ZipFile(export_path, "w") as zf:
        import json

        metadata: dict[str, Any] = {
            "litter": litter.dict(),
            "kittens": [kitten.dict() for kitten in kittens],
            "attachments": [attachment.dict() for attachment in attachments],
        }
        zf.writestr("metadata.json", json.dumps(metadata, default=str, indent=2))
        for attachment in attachments:
            path = Path(attachment.file_path)
            if path.exists():
                zf.write(path, arcname=path.name)

    return FileResponse(export_path)
