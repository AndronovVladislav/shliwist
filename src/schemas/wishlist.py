from pydantic import BaseModel


class WishlistItemBase(BaseModel):
    title: str
    price: float
    link: str
    description: str


class WishlistItemCreateRequest(WishlistItemBase):
    pass


class WishlistItemResponse(WishlistItemBase):
    id: int
    donor_id: int | None
    is_active: bool

    model_config = {
        'from_attributes': True
    }


class WishlistItemUpdateRequest(BaseModel):
    title: str | None = None
    price: float | None = None
    link: str | None = None
    description: str | None = None
