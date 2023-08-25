import psycopg2
from psycopg2 import sql

host = 'xxx'
dbname = "xxx"
user = "xxx"
password = "xxx"

connection = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)

def create_db():

    try:
        # Create a cursor
        cursor = connection.cursor()

        table_name = "example_table"

            # Create the table if it doesn't exist
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                column1 VARCHAR,
                column2 VARCHAR
            );
        """).format(sql.Identifier(table_name))

        cursor.execute(create_table_query)
        connection.commit()

        # Insert data into the table
        insert_query = sql.SQL("""
            INSERT INTO {} (column1, column2) VALUES (%s, %s);
        """).format(sql.Identifier(table_name))

        values = ("value1", "value2")
        cursor.execute(insert_query, values)
        connection.commit()

    except Exception as e:
        print("Error:", e)
        connection.rollback()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

def check_db():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM example_table"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(row)
    except Exception as e:
        print('Error', e)
        connection.rollback()
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == '__main__':
    # create_db()
    check_db()