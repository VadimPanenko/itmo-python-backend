from __future__ import annotations
from dataclasses import field
from dataclasses import dataclass
from typing import List

from lecture_2.hw.shop_api.api.item.contracts import (
    ItemRequest
)

@dataclass(slots=True)
class Item:
    id: int
    name: str
    price: float
    deleted: bool = False

    @staticmethod
    def from_request(id: int, request: ItemRequest) -> Item:
        new_item = Item(id=id, name=request.name,
                        price=request.price)

        return new_item
    
    def update_name(self, name) -> None:
        self.name = name

    def update_price(self, price) -> None:
        self.price = price

    def update(self, request) -> None:
        self.update_name(request.name)
        self.update_price(request.price)

@dataclass(slots=True)
class CartItem:
    id: int
    item_name: str
    quantity: int
    available: bool

    @staticmethod
    def from_item(item: Item) -> CartItem:
        return CartItem(
            id = item.id,
            item_name = item.name,
            quantity = 1,
            available = True
        )

@dataclass(slots=True)
class Cart:
    id: int
    items: List[CartItem] = field(default_factory=list)
    price: float = 0.0

    @staticmethod
    def from_id(id: int) -> Cart:
        return Cart(id=id)
