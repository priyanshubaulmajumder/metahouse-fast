from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List, Type, Dict, Any
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

class ModalGenericService:
    @staticmethod
    async def safe_bulk_create(db: AsyncSession, model: Type[Any], objs: List[Dict[str, Any]]):
        try:
            db.add_all([model(**obj) for obj in objs])
            await db.commit()
        except IntegrityError:
            await db.rollback()
            for obj in objs:
                try:
                    merged_obj = await db.merge(model(**obj))
                    await db.commit()
                except IntegrityError:
                    await db.rollback()

    @staticmethod
    async def optimized_update(
        db: AsyncSession,
        model: Type[Any],
        uid_col_mapping: Dict[str, str],
        unique_ids: List[str],
        rows_to_update: List[Dict[str, Any]],
        additional_condition=None
    ):
        stmt = insert(model).values(rows_to_update)
        update_dict = {c.name: c for c in stmt.excluded if c.name not in unique_ids}
        stmt = stmt.on_conflict_do_update(
            index_elements=[getattr(model, uid_col_mapping[uid]) for uid in unique_ids],
            set_=update_dict
        )
        if additional_condition is not None:
            stmt = stmt.where(additional_condition)
        await db.execute(stmt)
        await db.commit()
