import psycopg as database_driver
import contextlib
import app.config as appconfig

settings: appconfig.Settings = appconfig.get_settings()

postgres_dsn = {
    "host": settings.db_server,
    "port": settings.db_port,
    "user": settings.db_uid,
    "password": settings.db_pid,
    "dbname": settings.db_name,
}


@contextlib.contextmanager
def dbconnect(database_dsn: dict = postgres_dsn):
    """
    Returns a Database Cursor that SQL Quries can be executed against.
    If connection is unsuccessful return None and check for validity
    within the context to ensure it is not None
    """
    print("Connecting to database...")
    conn = None
    curr = None
    try:
        conn = database_driver.connect(**database_dsn)
    except database_driver.OperationalError as error:
        print(error)
        yield None
    else:
        try:
            curr = conn.cursor()
        except database_driver.OperationalError as error:
            print(error)
            yield None
        else:
            yield curr
    finally:
        if conn:
            conn.commit()
        if curr:
            curr.close()
        if conn:
            conn.close()
        print("Database connection closed.")


def ResultIter(cursor, chunk_size=1000):
    "An iterator that uses fetchmany to keep memory usage down"
    column_names = [column_name[0] for column_name in cursor.description]
    while True:
        results = None
        if chunk_size == 0:
            results = cursor.fetchall()
        elif chunk_size == 1:
            results = cursor.fetchone()
        else:
            results = cursor.fetchmany(chunk_size)
        if not results:
            break
        if chunk_size == 1:
            yield {column[0]: column[1] for column in zip(column_names, results)}
        else:
            for result in results:
                yield {column[0]: column[1] for column in zip(column_names, result)}
