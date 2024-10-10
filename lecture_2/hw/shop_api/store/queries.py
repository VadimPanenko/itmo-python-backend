from typing import Iterable, List, Optional

from lecture_2.hw.shop_api.store.models import (
    Cart,
    Item,
    CartItem
)
from lecture_2.hw.shop_api.store.db import (
    _cart,
    _item
)
from lecture_2.hw.shop_api.api.item.contracts import (
    ItemRequest,
    ItemPatchRequest
)


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1

_id_generator_cart = int_id_generator()
_id_generator_item = int_id_generator()

def generate_new_cart() -> Cart:
    global _id_generator_cart
    _id = next(_id_generator_cart)
    new_cart = Cart.from_id(_id)
    _cart[_id] = new_cart

    return new_cart

def generate_new_item(item_request: ItemRequest) -> Item:
    global _id_generator_item
    _id = next(_id_generator_item)
    new_item = Item.from_request(_id, item_request)

    _item[_id] = new_item

    return new_item

def get_cart_from_id(id: int) -> Cart:
    return _cart[id]

def get_item_from_id(id: int) -> Item:
    return _item[id]

def raise_errors(offset: int,
                 limit: int,
                 min_max_list: list
                ) -> None:
    if offset < 0:
        raise ValueError("Offset must be a non-negative integer")
    if limit <= 0:
        raise ValueError("Limit must be a positive integer")
    if any([min_max is not None and min_max < 0 for min_max in min_max_list]):
        raise ValueError("Min/Max values must be a non-negative integer")
    
def get_carts(offset: int,
              limit: int,
              min_price: Optional[float],
              max_price: Optional[float],
              min_quantity: Optional[float],
              max_quantity: Optional[float]) -> List[Cart]:
    
    min_max_list = [min_price, max_price, min_quantity, max_quantity]
    raise_errors(offset,
                 limit,
                 min_max_list)
    
    if offset >= len(_cart):
        return []
    if offset + limit >= len(_cart):
        limit =  len(_cart) - offset

    filtered_carts = [
        _cart[cart_id] for cart_id in range(offset, offset+limit)
        if (min_price is None or _cart[cart_id].price >= min_price)
        and (max_price is None or _cart[cart_id].price <= max_price)
        and (min_quantity is None or 
             sum([item.quantity for item in _cart[cart_id].items]) >= min_quantity)
        and (max_quantity is None or 
             sum([item.quantity for item in _cart[cart_id].items]) <= max_quantity)
    ]

    return filtered_carts
    
def add_item_to_cart(cart_id: int, item_id: int) -> Cart:
    try:
        cart = get_cart_from_id(cart_id)
        added_item = get_item_from_id(item_id)
    except KeyError as k:
        raise ValueError(f"Cart with id {cart_id} or Item with id {item_id} are not found")

    for item in cart.items:
        if item.id == item_id and item.available:
            item.quantity += 1
            cart.price += added_item.price
            return cart

    new_item = CartItem.from_item(added_item)
    cart.items.append(new_item)
    cart.price += added_item.price

    return cart

def get_items(offset: int,
              limit: int,
              min_price: Optional[float],
              max_price: Optional[float],
              show_deleted: bool = False) -> List[Item]:
    
    min_max_list = [min_price, max_price]
    raise_errors(offset,
                 limit,
                 min_max_list)
    
    if offset >= len(_item):
        return []
    if offset + limit >= len(_item):
        limit =  len(_item) - offset

    filtered_items = [
        _item[item_id] for item_id in range(offset, offset+limit)
        if (min_price is None or _item[item_id].price >= min_price)
        and (max_price is None or _item[item_id].price <= max_price)
        and (show_deleted or not _item[item_id].deleted)
    ]

    return filtered_items

def update_item(item_id: int, item_request: ItemRequest) -> Item:
    item = get_item_from_id(item_id)

    if item.deleted:
        raise ValueError("Item was deleted")
    item.update(item_request)

    return item

def patch_item(item_id: int, item_request: ItemPatchRequest) -> Item:
    item = get_item_from_id(item_id)
    if item.deleted:
        raise ValueError("Item was deleted")

    if item_request.name is not None:
        item.update_name(item_request.name)

    if item_request.price is not None:
        item.update_price(item_request.price)

    return item

def delete_item(item_id: int):
    item = get_item_from_id(item_id)
    item.deleted = True