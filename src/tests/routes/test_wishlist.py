import pytest
from httpx import AsyncClient

from src.models import WishlistItem
from src.schemas.wishlist import WishlistItemResponse


@pytest.mark.asyncio
async def test_create_wishlist_item(client: AsyncClient):
    reference = {
        'title': 'Test Item',
        'price': 123.45,
        'link': 'https://example.com',
        'description': 'A test wishlist item'
    }
    response = await client.post('/wishlist/', json=reference)
    assert response.status_code == 201
    data = response.json()

    for item, value in reference.items():
        assert data[item] == value
    assert data['donor_id'] is None
    assert data['is_active'] is True


@pytest.mark.asyncio
async def test_get_my_wishlist(client: AsyncClient, wishlist_item_1: WishlistItem):
    response = await client.get('/wishlist/')
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0] == WishlistItemResponse.model_validate(wishlist_item_1).model_dump()


@pytest.mark.asyncio
async def test_update_wishlist_item(client: AsyncClient, wishlist_item_1: WishlistItem):
    response = await client.patch(f'/wishlist/{wishlist_item_1.id}', json={'title': 'Updated'})
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated'


@pytest.mark.asyncio
async def test_delete_wishlist_item(client: AsyncClient, wishlist_item_1: WishlistItem):
    response = await client.delete(f'/wishlist/{wishlist_item_1.id}')
    assert response.status_code == 204
