import unittest
import reports
from tablib import Dataset
from unittest.mock import MagicMock, patch


class TestDBConnection(unittest.TestCase):

    def test_connection(self):
        # reports.io.Connection object
        conn = reports.io.Connection()
        self.assertIsInstance(conn, reports.io.Connection)

    def test_sqllite_connection(self):
        # Simulate reports.io.SQLliteConnection object
        conn = MagicMock()
        with patch(target='sqlite3.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.database = 'mydb.db'
            self.assertEqual(conn.connection.database, 'mydb.db')
            # Test close
            conn.cursor.close()

    def test_mysql_connection(self):
        # Simulate reports.io.MySQLConnection object
        conn = MagicMock()
        with patch(target='mysql.connector.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.host = 'mysqldb.local'
            conn.connection.database = 'mydb'
            conn.connection.username = 'username'
            conn.connection.password = 'password'
            conn.connection.port = 3306
            self.assertEqual(conn.connection.host, 'mysqldb.local')
            self.assertEqual(conn.connection.database, 'mydb')
            self.assertEqual(conn.connection.username, 'username')
            self.assertEqual(conn.connection.password, 'password')
            self.assertEqual(conn.connection.port, 3306)
            # Test close
            conn.cursor.close()

    def test_mssqldb_connection(self):
        # Simulate reports.io.MSSQLConnection object
        conn = MagicMock()
        with patch(target='pymssql.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.host = 'mssqldb.local'
            conn.connection.database = 'mydb'
            conn.connection.username = 'username'
            conn.connection.password = 'password'
            conn.connection.port = 1433
            self.assertEqual(conn.connection.host, 'mssqldb.local')
            self.assertEqual(conn.connection.database, 'mydb')
            self.assertEqual(conn.connection.username, 'username')
            self.assertEqual(conn.connection.password, 'password')
            self.assertEqual(conn.connection.port, 1433)
            # Test close
            conn.cursor.close()

    def test_postgresqldb_connection(self):
        # Simulate reports.io.PostgreSQLConnection object
        conn = MagicMock()
        with patch(target='psycopg2.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.host = 'postgresqldb.local'
            conn.connection.database = 'mydb'
            conn.connection.username = 'username'
            conn.connection.password = 'password'
            conn.connection.port = 5432
            self.assertEqual(conn.connection.host, 'postgresqldb.local')
            self.assertEqual(conn.connection.database, 'mydb')
            self.assertEqual(conn.connection.username, 'username')
            self.assertEqual(conn.connection.password, 'password')
            self.assertEqual(conn.connection.port, 5432)
            # Test close
            conn.cursor.close()


class TestDBManager(unittest.TestCase):
    conn = MagicMock()
    with patch(target='psycopg2.connect') as mock:
        conn.connection = mock.return_value
        conn.cursor = conn.connection.cursor.return_value
        conn.connection.host = 'postgresqldb.local'
        conn.connection.database = 'mydb'
        conn.connection.username = 'username'
        conn.connection.password = 'password'
        conn.connection.port = 5432

    def test_db_manager(self):
        # Test database manager
        db_manager = reports.io.DatabaseManager(connection=self.conn)
        self.assertIsInstance(db_manager, reports.io.DatabaseManager)
        # Test reconnect
        db_manager.reconnect()
        # Test SELECT query
        db_manager.execute('SELECT * from test')
        data = db_manager.fetchall()
        self.assertIsInstance(data, Dataset)
        # Test store procedure
        db_manager.callproc('myproc')
        data = db_manager.fetchone()
        self.assertIsInstance(data, Dataset)


if __name__ == '__main__':
    unittest.main()
