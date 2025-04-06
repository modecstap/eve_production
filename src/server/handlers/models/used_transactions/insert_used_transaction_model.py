from pydantic import BaseModel


class InsertUsedTransactionModel(BaseModel):
    product_id: int
    transaction_id: int
    used_count: int
