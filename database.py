import psycopg2 as psycopg2
from psycopg2.extras import DictCursor

host = "ec2-34-249-161-200.eu-west-1.compute.amazonaws.com"
user = "xmdvmccclcsnaq"
password = "00383ec4065ff55e9a6b9faf952e6b1c7f2932dd51d4697420f2792bdaaac8e2"
db_name = "dd6ppfn1k34232"

# connect to exist database
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True


def get_cursor():
    return connection.cursor(cursor_factory=DictCursor)


def create_table(table_name, values):
    cur = get_cursor()
    try:
        cur.execute(f"""CREATE TABLE {table_name} ({values})""")
    except Exception as ex:
        print(ex)
    finally:
        cur.close()


def check_table(table_name, columns, wh_col, wh_val):
    result = select_values_from_table(table_name, columns, wh_col, wh_val)
    if result:
        return True
    else:
        return False


def insert_values_in_table(table_name, columns, values):
    # columns, values,
    cur = get_cursor()
    try:
        cur.execute(f"""
            INSERT INTO {table_name}({columns}) 
            VALUES ({values});
            """)

    except Exception as ex:
        print('kakogo')
        print(ex)
    finally:
        cur.close()


def update_table_values(table_name, column, new_value, wh_col1, wh_val1, wh_col2='', wh_val2='', and_val=''):
    cur = get_cursor()
    if and_val != '':
        text = f"""UPDATE {table_name} SET {column}= '{new_value}' WHERE {wh_col1} = '{wh_val1}' AND {wh_col2} = 
        '{wh_val2}';"""
    else:
        text = f"""UPDATE {table_name} SET {column}= '{new_value}' WHERE {wh_col1} = '{wh_val1}';"""

    try:
        cur.execute(text)
    except Exception as ex:
        print('kakogo')
        print(ex)
    finally:
        cur.close()


# print(select_values_from_table('t515865796', '*', 'date_of_the_event', '2023', 'yes'))
def select_values_from_table(table_name, columns, wh_col, wh_val, like='', order=''):
    cur = get_cursor()
    where_txt = ''

    if wh_col != '':
        where_txt = f"WHERE {wh_col} = '{wh_val}'"

    if like != '':
        where_txt = f"WHERE {wh_col} LIKE '%{wh_val}%'"

    if order != '':
        where_txt += f' ORDER BY {wh_col};'

    try:
        cur.execute(f"""
            SELECT {columns} FROM {table_name}
            {where_txt};
            """, )
    except Exception as ex:
        print(ex)
    finally:
        res = cur.fetchall()
        cur.close()
    return res


def delete_values_from_table(table_name, wh_col1, wh_val1, wh_col2, wh_val2):
    cur = get_cursor()

    where_txt = f"WHERE {wh_col1} = '{wh_val1}' AND {wh_col2} = '{wh_val2}'"

    try:
        cur.execute(f"""
            DELETE FROM {table_name}
            {where_txt};
            """, )
    except Exception as ex:
        print(ex)
    finally:
        cur.close()
