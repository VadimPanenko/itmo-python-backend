from http import HTTPStatus
from fastapi import APIRouter, Response, HTTPException

from lecture_2.hw.shop_api.store import (
    Item,
    generate_new_item,
    get_item_from_id,
    get_items,
    update_item,
    patch_item,
    delete_item
)
from .contracts import (
    ItemRequest,
    ItemPatchRequest
)
from typing import Optional, List

router = APIRouter(prefix="/item")

@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully added new item",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to add new item",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Item,
)
async def create_item(item_request: ItemRequest, response: Response) -> Item:
    item = generate_new_item(item_request)
    response.headers["location"] = f"/item/{item.id}"

    return item

@router.get(
    "/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def get_item(item_id: int) -> Item:
    try:
        item = get_item_from_id(item_id)
        if item.deleted:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item with this id was deleted")
    except KeyError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item with this id is not found")
    return item

@router.get(
    "/",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned lists of requested items",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested items",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[Item],
)
async def get_list_items(offset: int = 0,
                         limit: int = 10,
                         min_price: Optional[float] = None,
                         max_price: Optional[float] = None,
                         show_deleted: bool = False
                         ) -> List[Item]:
    try:
        list_of_items = get_items(offset,
                                  limit,
                                  min_price,
                                  max_price,
                                  show_deleted)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"{e}")
    if list_of_items is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Items not found")
    return list_of_items

@router.put(
    "/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Data in item was successfully changed",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to change data",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def update_item_from_id(item_id: int, item_request: ItemRequest) -> Item:
    try:
        item = update_item(item_id, item_request)
    except KeyError:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return item

@router.patch(
    "/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Data in item was successfully changed",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to change data",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def patch_item_from_id(item_id: int, item_request: ItemPatchRequest) -> Item:
    try:
        item = patch_item(item_id, item_request)
    except KeyError:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED, detail=str(e))
    return item

@router.delete(
    "/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Item was successfully deleted"
            },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to delete item"
            },
    },
    status_code=HTTPStatus.OK,
)
async def delete_item_from_id(item_id: int):
    try:
        item = delete_item(item_id)
    except KeyError:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    return item
