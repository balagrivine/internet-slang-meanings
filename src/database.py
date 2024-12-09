from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

class InitDB:
    """Initializes a postgresql database connection"""

    def __init__(self):
        self.db_name: str = os.getenv("DB_NAME", "internetslang")
        self.db_user: str = os.getenv("DB_USER", "postgres")
        self.db_password: str = os.getenv("DB_PASSWORD", "postgres")
        self.db_port: int = os.getenv("DB_PORT", 5432)
        self.db_host: str = os.getenv("DB_HOST", "localhost")

        self.conn = None # Database connection

        """This method makes a connection to the database"""
        try:
            # Use as context manager to close the connection
            # automatically afterwards
            conn = psycopg.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port,
                host=self.db_host
            )
            self.conn = conn
        except psycopg.OperationalError as e:
            print("Failed to connect to the database")
            raise e

    def close_connection(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Destructor to close the connection when object is destroyed"""
        self.close_connection()

    def get_slang_meaning(self, slang_abbreviation: str):
        """Retrieves the meaning of a text abbreviation"""

        sql_context = """
        SELECT
            meaning
        FROM
            text_abbreviations
        WHERE
            abbreviation = %s;
        """
        data = (slang_abbreviation,)
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql_context, data)
                result = cursor.fetchone()

            self.conn.commit()
            return result
        except psycopg.DataError as e:
            print(e)

db_conn = InitDB()
