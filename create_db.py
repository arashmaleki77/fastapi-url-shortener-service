from sqlalchemy_utils import create_database, database_exists
from core.settings import settings


if __name__ == "__main__":
    print("create databases started.")

    all_db_names = [settings.POSTGRES_DB, "test_db"]
    for db_name in all_db_names:
        try:
            db_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{db_name}"
            if not database_exists(db_url):
                print(f"DB Name: {db_name}")
                create_database(db_url)
        except Exception as error:
            print(f"Error on creating database {db_name}", error)

    print("create databases ended.")
