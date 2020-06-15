import psycopg2
import json
from psycopg2.extras import RealDictCursor
from setting import host, port, user, password, db_name

conn = psycopg2.connect(host=host, port=port, database=db_name, user=user, password=password, cursor_factory=RealDictCursor)
cursor = conn.cursor()

# fake bin weight
def resetFakeBinWeight(bin_id=None):
    if bin_id == None:
        postgreSQL_delete_Query = "DELETE FROM fake_bins_weight"
        cursor.execute(postgreSQL_delete_Query)
        conn.commit()
        return "reset all success"
    else:
        postgreSQL_delete_Query = "DELETE FROM fake_bins_weight where bin_id = %s"
        cursor.execute(postgreSQL_delete_Query, (bin_id,))
        conn.commit()
        return "reset " + bin_id + " success"


def findfakeBinExists(bin_id):
    postgreSQL_select_Query = "select * from fake_bins_weight where bin_id = %s"
    cursor.execute(postgreSQL_select_Query, (bin_id,))
    result = cursor.fetchone()
    if result == None:
        return 1
    else:
        return 0


def findfakeBinWeight(bin_id):
    postgreSQL_select_Query = "select * from fake_bins_weight where bin_id = %s"
    cursor.execute(postgreSQL_select_Query, (bin_id,))
    result = cursor.fetchone()
    print("the the weight",result)
    if result == None:
        return 0
    else:
        return int(result['weight'])


def CreateUpdatefakeBinWeight(bin_id, weight, check):
    if check == 1:
        #     print("no bin id exists,will create new one")
        cursor.execute("insert into fake_bins_weight (bin_id, weight) values (%s, %s) RETURNING id", (bin_id, weight))
        conn.commit()
        return "created"
    else:
        cursor.execute("update fake_bins_weight set weight = %s where bin_id = %s", (weight, bin_id))
        conn.commit()
        return "updated"


def CreateTest():
    print("no bin id exists,will create new one")
    cursor.execute("insert into fake_bins_weight (bin_id, weight) values (%s, %s) RETURNING id", ("My001", 20))
    conn.commit()
    return "created"
