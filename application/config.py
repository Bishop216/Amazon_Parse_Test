try:
    import application.local as local
except ImportError:
    raise RuntimeError("Database credentials are not provided!")

product_url = "https://www.amazon.com/dp/{}"
product_all_reviews_url = "https://www.amazon.com/product-reviews/{}/?&filterByStar=all_stars"
product_positive_reviews_url = "https://www.amazon.com/product-reviews/{}/?&filterByStar=positive"


class Config:
    """
    Database configuration.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
