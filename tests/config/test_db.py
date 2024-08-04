import uuid
from datetime import datetime

import pytest
from sqlalchemy import DateTime, String, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from core.config.db import BaseModel, Base
from tests.conftest import engine


@pytest.fixture(scope="function")
async def model_for_test():
    class TestModel(BaseModel):
        __tablename__ = "test_model"
        string: Mapped[str] = mapped_column(String(50), nullable=True)
        integer: Mapped[int] = mapped_column(Integer, nullable=True)
        datetime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
        bool: Mapped[bool] = mapped_column(Boolean, nullable=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=[TestModel.__table__])

    return TestModel

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, tables=[TestModel.__table__])


class TestBaseModel:
    async def test_save(self, model_for_test):
        instance = model_for_test(string="test_save_1")
        assert instance.string == "test_save_1"
        await instance.save()
        assert instance.id, f"Instance id: {instance.id}"
        assert instance.created_at, f"Instance created_at: {instance.created_at}"
        assert instance.updated_at, f"Instance updated_at: {instance.updated_at}"
        assert instance.pk == instance.id, f"Instance pk: {instance.pk}"
        instance.string = "test_save_2"
        await instance.save()
        assert instance.string == "test_save_2", f"Instance string: {instance.string}"

    async def test_update(self, model_for_test):
        instance = model_for_test(string="test_update_1")
        await instance.save()
        await instance.update(**{
            "string": "test_update_2",
            "bool": True,
        })
        assert instance.string == "test_update_2", f"Instance string: {instance.string}"


class TestModelManager:
    async def test_get_by_id(self, model_for_test):
        instance = model_for_test(string="test")
        await instance.save()
        instance_ = await model_for_test.objects.get_by_id(instance.pk)
        assert instance_.string == "test", f"Instance string: {instance_.string}"
        assert instance_.id == instance.id, f"Instance id: {instance_.id}"
        with pytest.raises(model_for_test.NotFoundError):
            await model_for_test.objects.get_by_id(uuid.uuid4()), "Instance not found"

    async def test_get(self, model_for_test):
        await model_for_test(string="test_get").save()
        instance = await model_for_test.objects.get(string="test_get")
        assert instance.string == "test_get", f"Instance string: {instance.string}"
        with pytest.raises(model_for_test.NotFoundError):
            await model_for_test.objects.get(string="test_get_none"), "Instance not found"
        await model_for_test(string="test_get").save()
        with pytest.raises(model_for_test.MultipleObjectsReturned):
            await model_for_test.objects.get(string="test_get")

    async def test_all(self, model_for_test):
        await model_for_test(string="test").save()
        await model_for_test(string="tes1").save()
        await model_for_test(string="tes2").save()
        instances = await model_for_test.objects.all()
        assert len(instances) >= 3, f"Instances count: {len(instances)}"

    async def test_filter(self, model_for_test):
        await model_for_test(string="test", integer=1).save()
        await model_for_test(string="tes1", integer=2).save()
        await model_for_test(string="tes2", integer=2).save()
        await model_for_test(string="tes2", integer=3).save()
        instances = await model_for_test.objects.filter(integer=2)
        assert len(instances) == 2, f"Instances count: {len(instances)}"

    async def test_get_or_create(self, model_for_test):
        name = 'test_get_or_create'
        instance, created = await model_for_test.objects.get_or_create(string=name)
        assert instance.string == name, f"Instance string: {instance.string}"
        assert created, f"Instance created: {created}"
        instance_, created = await model_for_test.objects.get_or_create(string=name)
        assert not created, f"Instance created: {created}"
        assert instance.pk == instance_.pk, f"Instance pk: {instance_.pk}"

    async def test_update_or_create(self, model_for_test):
        instance, created = await model_for_test.objects.update_or_create(string="test")
        assert instance.string == "test", f"Instance string: {instance.string}"
        instance_, created = await model_for_test.objects.update_or_create(string="test", integer=1)
        assert instance_.string == "test", f"Instance string: {instance_.string}"
        assert instance_.integer == 1, f"Instance integer: {instance_.integer}"
        assert instance.id != instance_.id, f"Instance id: {instance_.id}"
        instance_, created = await model_for_test.objects.update_or_create(string="test", integer=2)
        assert instance.id != instance_.id, f"Instance id: {instance_.id}"
        assert instance.pk != instance_.pk, f"Instance pk: {instance_.pk}"

    async def test_create(self, model_for_test):
        instance = await model_for_test.objects.create(string="test")
        assert instance.string == "test", f"Instance string: {instance.string}"
        assert instance.id, f"Instance id: {instance.id}"
        instance_ = await model_for_test.objects.create(string="test2")
        assert instance_.string == "test2", f"Instance string: {instance_.string}"
        assert instance.pk != instance_.pk, f"Instance pk: {instance.pk}"

    async def test_bulk_create(self, model_for_test):
        instances = [
            model_for_test(string="test"),
            model_for_test(string="test2"),
            model_for_test(string="test3"),
        ]
        await model_for_test.objects.bulk_create(instances)
        instances_ = await model_for_test.objects.all()
        assert len(instances_) >= 3, f"Instances count: {len(instances_)}"
