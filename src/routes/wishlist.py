from fastapi import APIRouter, Depends

from src.routes.auth.validation import get_current_username
from src.schemas.wishlist import WishlistItemResponse, WishlistItemCreateRequest, WishlistItemUpdateRequest
from src.services.user import (
    get_user_wishlist as get_user_wishlist_service,
    create_wishlist_item as create_wishlist_item_service,
    assign_wishlist_item as assign_wishlist_item_service,
    update_wishlist_item as update_wishlist_item_service,
    delete_wishlist_item as delete_wishlist_item_service,
)

router = APIRouter(prefix='/wishlist', tags=['Wishlist'])


@router.get('/', response_model=list[WishlistItemResponse])
async def get_user_wishlist(username: str = Depends(get_current_username)):
    return await get_user_wishlist_service(username)


@router.post('/', status_code=201)
async def create_wishlist_item(item: WishlistItemCreateRequest, username: str = Depends(get_current_username)):
    return await create_wishlist_item_service(item, username)


@router.post('/{item_id}/assign', response_model=WishlistItemResponse)
async def assign_wishlist_item(item_id: int, username: str = Depends(get_current_username)):
    return await assign_wishlist_item_service(item_id, username)


@router.patch('/{item_id}', response_model=WishlistItemResponse)
async def update_wishlist_item(item_id: int,
                               update: WishlistItemUpdateRequest,
                               username: str = Depends(get_current_username),
                               ):
    return await update_wishlist_item_service(item_id, update, username)


@router.delete('/{item_id}', status_code=204)
async def delete_wishlist_item(item_id: int, username: str = Depends(get_current_username)):
    await delete_wishlist_item_service(item_id, username)
