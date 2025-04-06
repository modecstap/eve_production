from pydantic import BaseModel


class UsedTransactionModel(BaseModel):
    product_id: int
    transaction_id: int
    used_count: int
