import mysql.connector
from mysql.connector import Error


class DbManager:
    def __init__(self, close_after=False):
        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="eli",
                password="3010",
                database="inflow"
            )

            self.close_after = close_after

            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Connected to MySQL database")

        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None
            self.cursor = None

    def insert(self, query, data=()):
        if not self.conn or not self.cursor:
            print("Insert failed: No database connection.")
            return False

        try:
            self.cursor.execute(query, data)
            self.conn.commit()

            return self.cursor.lastrowid

        except Error as e:
            print("Error in SQL insert:", e)
            return False

        finally:
            if self.close_after:
                self.close()

    def select(self, query, data=(), fetch_one=False):
        if not self.conn or not self.cursor:
            print("Select failed: No database connection.")
            return None

        try:
            self.cursor.execute(query, data)
            return self.cursor.fetchone() if fetch_one else self.cursor.fetchall()

        except Error as e:
            print(f"Error in SQL select: {e}")
            return None

        finally:
            if self.close_after:
                self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
