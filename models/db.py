from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
from api.v2.app import logging


class DatabaseManager:
    def __init__(self, db_url, db_name):
        """
        Initializes a new instance of the DatabaseManager class.

        Args:
            db_url (str): The URL of the database.
            db_name (str): The name of the database.

        Returns:
            None
        """
        self.db_url = db_url
        self.db_name = db_name
        self.engine = create_engine(db_url)
        logging.info(f"Database initialized : {db_url} {db_name}")
        self._initialize_db()
        self.engine_with_db = create_engine(f"{db_url}{db_name}", echo=False)

    def _initialize_db(self):
        """
        Initializes the database by creating it if it does not exist.

        Args:
            None

        Returns:
            None
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS {self.db_name}"))
                logging.info(
                    f"Database '{self.db_name}' created successfully.")

        except ProgrammingError as e:
            logging.error(f"Error: {e}")

    def get_session(self):
        """
        Retrieves a new database session.

        Args:
            None

        Returns:
            session: A new database session with autocommit and autoflush
            disabled.
        """
        return sessionmaker(autocommit=False, autoflush=False,
                            bind=self.engine_with_db)()
