import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, WishlistItem
from src.models.utils import connection
from src.schemas.wishlist import WishlistItemCreateRequest, WishlistItemUpdateRequest
from src.services.wishlist import (
    create_wishlist_item,
    assign_wishlist_item,
    update_wishlist_item,
    delete_wishlist_item
)


@pytest.mark.asyncio
async def test_create_wishlist_item(user_1: User):
    item_data = WishlistItemCreateRequest(title='item1', price=100.0, link='https://test.com', description='desc')
    result = await create_wishlist_item(item_data, user_1.username)
    assert result.title == 'item1'


@pytest.mark.asyncio
async def test_assign_wishlist_item_success(user_1: User, wishlist_item_2: WishlistItem):
    result = await assign_wishlist_item(wishlist_item_2.id, user_1.username)

    assert result.id == wishlist_item_2.id
    assert result.donor_id == user_1.id


@pytest.mark.asyncio
async def test_assign_wishlist_item_already_taken(user_1: User, wishlist_item_1: WishlistItem):
    wishlist_item_1.donor_id = 99

    with pytest.raises(HTTPException) as exc_info:
        await assign_wishlist_item(wishlist_item_1.id, user_1.username)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_update_wishlist_item_success(user_1: User, wishlist_item_1: WishlistItem):
    update_data = WishlistItemUpdateRequest(title='new')
    result = await update_wishlist_item(wishlist_item_1.id, update_data, user_1.username)

    assert result.title == 'new'


@pytest.mark.asyncio
async def test_delete_wishlist_item_success(user_1: User, wishlist_item_1: WishlistItem):
    await delete_wishlist_item(wishlist_item_1.id, user_1.username)
