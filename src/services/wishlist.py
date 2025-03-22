from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import User, WishlistItem
from src.models.utils import connection
from src.schemas.wishlist import WishlistItemResponse, WishlistItemCreateRequest, WishlistItemUpdateRequest


@connection
async def get_user(username: str, session: AsyncSession, with_wishlist: bool = False) -> User:
    q = select(User).where(User.username == username)
    if with_wishlist:
        q = q.options(selectinload(User.wishlist))

    user = (await session.execute(q)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
    return user


async def get_user_wishlist(username: str) -> list[WishlistItemResponse]:
    user = await get_user(username, with_wishlist=True)
    return [WishlistItemResponse.model_validate(item) for item in user.wishlist]


@connection
async def create_wishlist_item(item: WishlistItemCreateRequest,
                               username: str,
                               session: AsyncSession,
                               ) -> WishlistItemResponse:
    user = await get_user(username, session=session)
    new_item = WishlistItem(
        **item.model_dump(),
        acceptor_id=user.id
    )
    session.add(new_item)
    await session.flush()
    await session.refresh(new_item)
    return WishlistItemResponse.model_validate(new_item)


@connection
async def assign_wishlist_item(item_id: int, username: str, session: AsyncSession) -> WishlistItemResponse:
    user = await get_user(username, session=session)
    item = await session.get(WishlistItem, item_id)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Элемент не найден')
    if item.acceptor_id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Нельзя подарить самому себе')
    if item.donor_id is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Подарок уже занят')

    item.donor_id = user.id
    await session.flush()
    await session.refresh(item)
    return WishlistItemResponse.model_validate(item)


@connection
async def update_wishlist_item(item_id: int,
                               update: WishlistItemUpdateRequest,
                               username: str,
                               session: AsyncSession,
                               ) -> WishlistItemResponse:
    user = await get_user(username, session=session)
    item = await session.get(WishlistItem, item_id)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Элемент не найден')
    if item.acceptor_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Можно редактировать только свои подарки')

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    await session.flush()
    await session.refresh(item)
    return WishlistItemResponse.model_validate(item)


@connection
async def delete_wishlist_item(item_id: int, username: str, session: AsyncSession) -> None:
    user = await get_user(username, session=session)
    item = await session.get(WishlistItem, item_id)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Элемент не найден')
    if item.acceptor_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Можно удалять только свои подарки')

    await session.delete(item)
