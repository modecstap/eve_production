from enum import Enum


class EntityPrefix(str, Enum):
    TRANSACTIONS = "transactions"
    ORDERS = "orders"
    USED_TRANSACTIONS = "used_transactions"
    MATERIALS_LIST = "materials_list"
    PRODUCTS = "products"
    TYPES = "types"
    STATIONS = "stations"
