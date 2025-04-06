from pydantic import BaseModel


class UpdateUsedTransactionModel(BaseModel):
    product_id: int
    transaction_id: int
    used_count: int
