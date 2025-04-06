from pydantic import BaseModel


class UpdateUsedTransactionModel(BaseModel):
    product_id: int
    transaction_id: str
    used_count: int
