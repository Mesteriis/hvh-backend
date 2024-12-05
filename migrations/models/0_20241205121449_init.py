from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "usermodel" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "email" VARCHAR(256) NOT NULL UNIQUE,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "hashed_password" VARCHAR(1000),
    "last_login" TIMESTAMPTZ,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "date_joined" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "taskmodel" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "url" VARCHAR(256) NOT NULL,
    "status" VARCHAR(11) NOT NULL  DEFAULT 'new',
    "owner_id" UUID NOT NULL REFERENCES "usermodel" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_taskmodel_url_1d2707" ON "taskmodel" ("url");
COMMENT ON COLUMN "taskmodel"."status" IS 'new: new\npending: pending\nin_progress: in_progress\ncompleted: completed\nfailed: failed';
CREATE TABLE IF NOT EXISTS "channels" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "metadata" JSONB NOT NULL,
    "status" VARCHAR(11) NOT NULL  DEFAULT 'new',
    "ext_id" VARCHAR(256) NOT NULL UNIQUE,
    "owner_id" UUID NOT NULL REFERENCES "usermodel" ("id") ON DELETE CASCADE,
    "task_id" UUID NOT NULL REFERENCES "taskmodel" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_channels_status_f0dadf" ON "channels" ("status");
CREATE INDEX IF NOT EXISTS "idx_channels_ext_id_fe40e9" ON "channels" ("ext_id");
COMMENT ON COLUMN "channels"."status" IS 'new: new\npending: pending\nin_progress: in_progress\ncompleted: completed\nfailed: failed';
CREATE TABLE IF NOT EXISTS "playlists" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "metadata" JSONB NOT NULL,
    "status" VARCHAR(11) NOT NULL  DEFAULT 'new',
    "ext_id" VARCHAR(256) NOT NULL UNIQUE,
    "owner_id" UUID NOT NULL REFERENCES "usermodel" ("id") ON DELETE CASCADE,
    "task_id" UUID NOT NULL REFERENCES "taskmodel" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_playlists_status_adc1cc" ON "playlists" ("status");
CREATE INDEX IF NOT EXISTS "idx_playlists_ext_id_043ea8" ON "playlists" ("ext_id");
COMMENT ON COLUMN "playlists"."status" IS 'new: new\npending: pending\nin_progress: in_progress\ncompleted: completed\nfailed: failed';
CREATE TABLE IF NOT EXISTS "videos" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "metadata" JSONB NOT NULL,
    "status" VARCHAR(11) NOT NULL  DEFAULT 'new',
    "ext_id" VARCHAR(256) NOT NULL UNIQUE,
    "owner_id" UUID NOT NULL REFERENCES "usermodel" ("id") ON DELETE CASCADE,
    "task_id" UUID NOT NULL REFERENCES "taskmodel" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_videos_status_068cc9" ON "videos" ("status");
CREATE INDEX IF NOT EXISTS "idx_videos_ext_id_971380" ON "videos" ("ext_id");
COMMENT ON COLUMN "videos"."status" IS 'new: new\npending: pending\nin_progress: in_progress\ncompleted: completed\nfailed: failed';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
