import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много данных, которые вычислялись сто лет"


# запрос SQL в БД по определеному типу из БД
# select(operation).where(operation.c.type == operation_type) -
# тут мы обращаемся к таблице operation к одно из колонок type


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None,
        })


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"result": "success"}
