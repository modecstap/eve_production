from pydantic import BaseModel


class InsertUsedTransactionModel(BaseModel):
    product_id: int
    transaction_id: str
    used_count: int
