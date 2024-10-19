from tortoise import fields, models


class BaseDBModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["-created_at"]

    id = fields.UUIDField(unique=True, pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True, default=None)

    async def to_dict(self):
        d = {}
        for field in self._meta.db_fields:
            d[field] = getattr(self, field)
        for field in self._meta.backward_fk_fields:
            d[field] = await getattr(self, field).all().values()
        return d
