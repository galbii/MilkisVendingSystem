from pydantic import BaseModel, validator

class Item(BaseModel):
    item_name: str
    price: float
    item_company: str = ''
    quantity: int = 0
    slot: str = ''


    @classmethod
    def create_basic(cls, item_name: str, price: float):
        """
        Create a basic Product with default values for company and quantity.
        """
        return cls(item_name=item_name, price=price)

    @classmethod
    def create_with_quantity(cls, item_name: str, price: float, quantity: int):
        """
        Create a Product with a specified quantity.
        """
        return cls(item_name=item_name, price=price, quantity=quantity)

    @validator("slot")
    def validate_slot(cls, value):
        allowed_slots = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
        if value is not None and value not in allowed_slots:
            raise ValueError("Invalid slot. Allowed slots are: a1, a2, a3, b1, b2, b3, c1, c2, c3")
        return value

