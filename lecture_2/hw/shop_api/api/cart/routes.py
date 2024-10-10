from http import HTTPStatus
from fastapi import APIRouter, Response, HTTPException

from lecture_2.hw.shop_api.store import (
    Cart,
    generate_new_cart,
    get_cart_from_id,
    get_carts,
    add_item_to_cart
)
from typing import Optional, List

router = APIRouter(prefix="/cart")

@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully created new empty cart",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to created new empty cart",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Cart,
)
async def create_cart(response: Response) -> Cart:
    cart = generate_new_cart()
    response.headers["location"] = f"/cart/{cart.id}"

    return cart

@router.get(
    "/{cart_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Cart,
)
async def get_cart(cart_id: int) -> Cart:
    try:
        cart = get_cart_from_id(cart_id)
    except KeyError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cart with this id is not found")
    return cart

@router.get(
    "/",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned lists of requested carts",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested carts",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[Cart],
)
async def get_list_carts(offset: int = 0,
                         limit: int = 10,
                         min_price: Optional[float] = None,
                         max_price: Optional[float] = None,
                         min_quantity: Optional[float] = None,
                         max_quantity: Optional[float] = None
                         ) -> List[Cart]:
    try:
        list_of_carts = get_carts(offset,
                                  limit,
                                  min_price,
                                  max_price,
                                  min_quantity,
                                  max_quantity)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"{e}")
    if list_of_carts is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Carts not found")
    return list_of_carts

@router.post(
    "/{cart_id}/add/{item_id}",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully added item to cart",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to add item to cart",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Cart,
)
async def add_item_to_cart_from_id(cart_id: int, item_id: int) -> Cart:
    try:
        cart = add_item_to_cart(cart_id, item_id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return cart
