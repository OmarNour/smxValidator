import duckdb


def execute_query(con, query):
    try:
        result = con.sql(query).df()
        # result = duckdb.sql(query).df()
        return result
    except Exception as e:
        return str(e)
