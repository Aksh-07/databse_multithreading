import time
from threading import Semaphore, get_ident
import sqlite3
import concurrent.futures
from queue import Queue

s = time.time()

q = Queue()


def create_table():
    con = sqlite3.connect("practice.db")
    c = con.cursor()
    c.execute("""CREATE TABLE my_table (
    column1 INTEGER,
    column2 INTEGER,
    column3 INTEGER,
    column4 TEXT
    )""")
    con.commit()
    con.close()


def delete_table():
    con = sqlite3.connect("practice.db")
    c = con.cursor()
    c.execute("DROP TABLE my_table")
    con.commit()
    con.close()


def insert(lock_):
    con = sqlite3.connect("practice.db")
    c = con.cursor()
    while not q.empty():
        lock_.acquire()
        value = q.get()
        print(f"Thread_{get_ident()}, Pushing data into Database")
        c.execute("INSERT INTO my_table VALUES (?, ?, ?, ?)", value)
        lock_.release()
        con.commit()
    con.close()
    print(f"completed_{get_ident()}")
    if lock_._value == 4:
        fetch()


def fetch():
    con = sqlite3.connect("practice.db")
    c = con.cursor()
    c.execute("SELECT rowid, * FROM my_table")
    print(f"Thread_{get_ident()}, Fetching data from Database")

    items = c.fetchall()
    for item in items:
        print(f"{item[0]}: {item[1]} {item[2]} {item[3]} {item[4]}")
    con.close()


def convert_data(list_):
    for item_tuple in list_:
        item_tuple = eval(item_tuple)
        item_list = list(item_tuple)
        item_list[3] = str(item_list[3])
        new_item_tuple = tuple(item_list)
        q.put(new_item_tuple)


delete_table()
create_table()

with open("dataset.txt", "rt") as file:
    data = file.readlines()

convert_data(data)
lock = Semaphore(4)
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(insert, lock) for _ in range(4)]

f = time.time()
print(f"Total time: {f - s}")
