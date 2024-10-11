import psycopg2
from secret import database_password

def open_connection():
    conn = psycopg2.connect(
        database = "Telegrambot3",
        user = "postgres",
        password = database_password,
        host = "localhost",
        port= 5432
    )
    return conn

def close_connection(conn, cur):
    cur.close()
    conn.close()

def create_tables():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
                create table if not exists cars(
                car_id serial primary key,
                brand varchar(100) not null,
                model varchar(100) not null,
                year int not null);
                """)
    conn.commit()
    close_connection(conn, cur)
