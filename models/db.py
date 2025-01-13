from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError
from sqlalchemy import text
from api.v2.app import logging


class DatabaseManager:
    def __init__(self, db_url, db_name):
        """
        Initializes a new instance of the DatabaseManager class.

        Args:
            db_url (str): The URL of the database (excluding the database name).
            db_name (str): The name of the database.
        """
        self.db_url = db_url
        self.db_name = db_name

        try:
            # Initialize engine with server connection
            self.engine = create_engine(
                db_url,
                echo=False,
                pool_recycle=28000,  # Recycle connections to avoid timeout
                pool_pre_ping=True   # Check connections before use
            )
            logging.info(f"Database engine initialized for server: {db_url}")

            # Ensure the database exists
            self._initialize_db()

            # Initialize engine for the specific database
            full_db_url = f"{db_url}{db_name}"
            self.engine_with_db = create_engine(
                full_db_url,
                echo=False,
                pool_recycle=28000,
                pool_pre_ping=True
            )
            logging.info(f"Database engine initialized for {db_name}")

        except SQLAlchemyError as e:
            logging.error(f"Failed to initialize DatabaseManager: {e}")
            raise

    def _initialize_db(self):
        """
        Ensures the database exists. Creates it if it does not.

        Raises:
            SQLAlchemyError: If database creation fails.
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}`"))
                logging.info(
                    f"Database '{self.db_name}' ensured successfully.")
        except ProgrammingError as e:
            logging.error(
                f"Error while creating database '{self.db_name}': {e}")
            raise
        except SQLAlchemyError as e:
            logging.error(f"General SQLAlchemy error: {e}")
            raise

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
