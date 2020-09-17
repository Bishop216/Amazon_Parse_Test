try:
    import application.local as local
except ImportError:
    raise RuntimeError("Database credentials are not provided!")


class Config:
    """
    Database configuration.
    """
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://{login}:{pwd}@{db_host}:{db_port}/{db_name}"
        .format(
            login=local.login,
            pwd=local.password,
            db_host=local.database_host,
            db_port=local.database_port,
            db_name=local.database_name
        )
    )
