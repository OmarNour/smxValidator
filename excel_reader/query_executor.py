import duckdb


def execute_query(con, query):
    try:
        result = con.execute(query).fetchdf()
        return result
    except Exception as e:
        return str(e)
