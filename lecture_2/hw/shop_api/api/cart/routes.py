from http import HTTPStatus
from fastapi import APIRouter, Response, HTTPException
from typing import Optional, List

from lecture_2.hw.shop_api.store import (
    Cart,
    generate_new_cart,
    get_cart_from_id,
    get_carts,
    add_item_to_cart
)

router = APIRouter(prefix="/cart")

@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=Cart,
    responses={
        HTTPStatus.CREATED: {"description": "Successfully created new empty cart"},
        HTTPStatus.UNPROCESSABLE_ENTITY: {"description": "Failed to create new empty cart"},
    },
)
async def create_cart(response: Response) -> Cart:
    new_cart = generate_new_cart()
    response.headers["location"] = f"/cart/{new_cart.id}"
    return new_cart

@router.get(
    "/{cart_id}",
    status_code=HTTPStatus.OK,
    response_model=Cart,
    responses={
        HTTPStatus.OK: {"description": "Successfully returned requested cart"},
        HTTPStatus.NOT_FOUND: {"description": "Failed to return requested cart"},
    },
)
async def get_cart(cart_id: int) -> Cart:
    try:
        return get_cart_from_id(cart_id)
    except KeyError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cart with this id is not found")

@router.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=List[Cart],
    responses={
        HTTPStatus.OK: {"description": "Successfully returned list of requested carts"},
        HTTPStatus.NOT_FOUND: {"description": "Failed to return requested carts"},
    },
)
async def get_list_carts(
    offset: int = 0,
    limit: int = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_quantity: Optional[float] = None,
    max_quantity: Optional[float] = None
) -> List[Cart]:
    try:
        carts_list = get_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)
        if not carts_list:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Carts not found")
        return carts_list
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))

@router.post(
    "/{cart_id}/add/{item_id}",
    status_code=HTTPStatus.CREATED,
    response_model=Cart,
    responses={
        HTTPStatus.CREATED: {"description": "Successfully added item to cart"},
        HTTPStatus.UNPROCESSABLE_ENTITY: {"description": "Failed to add item to cart"},
    },
)
async def add_item_to_cart_from_id(cart_id: int, item_id: int) -> Cart:
    try:
        return add_item_to_cart(cart_id, item_id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
