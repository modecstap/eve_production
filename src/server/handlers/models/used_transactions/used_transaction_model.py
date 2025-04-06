from pydantic import BaseModel


class UsedTransactionModel(BaseModel):
    product_id: int
    transaction_id: str
    used_count: int
