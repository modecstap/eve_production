from abc import ABC

from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

from src.storage import Database


class AbstractTestApi(ABC):
    model: BaseModel
    entity: declarative_base
    db: Database
    client: TestClient

    def setup_db(self):
        pass

    def clear_db(self):
        pass

    def test_get_positive(self):
        pass

    def test_gets_positive(self):
        pass

    def test_insert_positive(self):
        pass

    def test_inserts_positive(self):
        pass

    def test_update_positive(self):
        pass

    def test_updates_positive(self):
        pass

    def test_delete_positive(self):
        pass

    def test_deletes_positive(self):
        pass

    def test_get_negative(self):
        pass

    def test_gets_negative(self):
        pass

    def test_insert_negative(self):
        pass

    def test_inserts_negative(self):
        pass

    def test_update_negative(self):
        pass

    def test_updates_negative(self):
        pass

    def test_delete_negative(self):
        pass

    def test_deletes_negative(self):
        pass

    def insert_into_db(self, entities):
        pass

    def get_from_db(self, entity_type, ids: list[int]):
        pass