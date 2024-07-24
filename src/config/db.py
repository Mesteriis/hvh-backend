#
# def create_engine():
#     db_settings = get_database_settings()
#     return create_engine_(db_settings)
#
#
# def create_session():
#     db_settings = get_database_settings()
#     return sessionmaker(
#         autocommit=db_settings.autocommit,
#         autoflush=db_settings.autoflush,
#         bind=create_engine(),
#     )
#
#
# engine = create_engine()
# session = create_session()
# Base = declarative_base()
