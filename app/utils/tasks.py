from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import get_idb
#from app.utils.ScoutService import ScoutService

app = FastAPI()

async def  update_mappings_for_scheme_task(wpc: str, db: AsyncSession):
    from app.models.scheme import Scheme
    from app.services.scheme import SchemeUniqueIDsCacheService

    if not wpc:
        return
    result = await db.execute(select(Scheme).filter(Scheme.wpc == wpc))
    obj = result.scalars().first()
    if obj:
        await SchemeUniqueIDsCacheService.update_all_mappings_for_scheme(obj=obj)

async def reset_cache_keys_affected_by_scheme_update_task(wpc: str, db: AsyncSession):
    from app.models.scheme import Scheme, SchemeAudit
    from app.services.cache import CacheKeysService

    if not wpc:
        return
    result = await db.execute(select(Scheme).filter(Scheme.wpc == wpc))
    obj = result.scalars().first()
    result = await db.execute(select(SchemeAudit).filter(SchemeAudit.wpc == wpc).order_by(SchemeAudit.created_at.desc()))
    sa_obj = result.scalars().first()
    if obj:
        await CacheKeysService.reset_keys_affected_by_scheme_update(obj)
    if sa_obj:
        await CacheKeysService.reset_keys_affected_by_scheme_update(sa_obj)

@app.post("/update_mappings_for_scheme/")
async def update_mappings_for_scheme(wpc: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_idb)):
    background_tasks.add_task(update_mappings_for_scheme_task, wpc, db)
    return {"message": "Task to update mappings for scheme has been initiated."}

@app.post("/reset_cache_keys_affected_by_scheme_update/")
async def reset_cache_keys_affected_by_scheme_update(wpc: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_idb)):
    background_tasks.add_task(reset_cache_keys_affected_by_scheme_update_task, wpc, db)
    return {"message": "Task to reset cache keys affected by scheme update has been initiated."}