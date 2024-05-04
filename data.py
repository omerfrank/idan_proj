import sqlite3

def objA(cursor):
    cursor.execute("SELECT * FROM Albums where AlbumId == 100")
    rows = cursor.fetchall()
    print(rows[0][1])

def objB(cursor):
    table_name = "Customers"
    cursor.execute(f"PRAGMA table_info({table_name})")

    # Fetch all the rows from the cursor
    columns_info = cursor.fetchall()

    # Loop through the columns information to find the primary key
    primary_key = None
    for column in columns_info:
        if column[5] == 1:  # The 'pk' column (index 5) will be 1 if it's a primary key
            primary_key = column[1]  # Column name is at index 1
            break

    if primary_key:
        print(primary_key)

def objC(cursor):
    cursor.execute("SELECT * FROM Site")
    rows = cursor.fetchall()
    print(rows)
def objD(cursor):
    cursor.execute("SELECT * FROM Customers where CustomerId == 37")
    rows = cursor.fetchall()
    print(rows[0][8])
def objE(cursor):
    table_name = "tracks"
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    print(cursor.fetchall())
def objF(cursor):
    cursor.execute(f"SELECT Name FROM tracks where TrackId == 5")
    print(cursor.fetchall())
def objG(cursor):
    cursor.execute(f"SELECT * FROM tracks where Composer == 'Alanis Morissette'")
    print(len(cursor.fetchall()))
def objH(cursor):
    cursor.execute(f"SELECT Composer FROM tracks where Name == 'Out Of Exile'")
    print((cursor.fetchall()))
def objI(cursor):
    cursor.execute(f"SELECT GenreId FROM tracks where Name == 'Out Of Exile'")
    id = cursor.fetchall()[0]
    cursor.execute(f"SELECT Name FROM genres where GenreId == {id[0]}")
    print((cursor.fetchall()))
        
        
conn = sqlite3.connect(r'C:\Users\omerf\OneDrive\שולחן העבודה\idan_proj\URL_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')


objC(cursor=cursor)

cursor.close()
conn.close()