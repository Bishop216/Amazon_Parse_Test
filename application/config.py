import os
import logging

try:
    import application.local as local
except ImportError:
    raise RuntimeError("Database credentials are not provided!")

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename=os.path.join(BASEDIR, "logs.log"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s: %(levelname)s: %(message)s"
)

logger = logging.getLogger()

product_url = "https://www.amazon.com/dp/{}"
product_all_reviews_url = "https://www.amazon.com/product-reviews/{}/?&filterByStar=all_stars"
product_positive_reviews_url = "https://www.amazon.com/product-reviews/{}/?&filterByStar=positive"

ALLOWED_EXTENSIONS = {'csv'}


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
