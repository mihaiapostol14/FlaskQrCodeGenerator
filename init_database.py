import pymysql
from urllib.parse import urlparse
from app import app, db  # Import Flask app and SQLAlchemy instance


def init_database():
    """
    Connects to the MySQL server, creates the database if it doesn't exist,
    and initializes all application tables.
    """
    # Retrieve the database connection URI from the Flask configuration
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']

    # Parse the URI to separate host, user, password, and database name
    parsed_url = urlparse(db_uri.replace('mysql+pymysql://', 'mysql://'))

    username = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port or 3306
    db_name = parsed_url.path.lstrip('/')

    # Connect directly to the MySQL server without specifying the database name
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        port=port,
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            # Create the database if it does not already exist
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"Database '{db_name}' has been successfully verified/created.")
    finally:
        connection.close()

    # Create all tables and columns within the Flask application context
    with app.app_context():
        db.create_all()
        print("Database tables and fields initialized successfully!")


if __name__ == '__main__':
    init_database()
