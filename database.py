import psycopg2

from load import BOT_TOKEN, BOT_TOKEN, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def get_connect():
    return psycopg2.connect(
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )


def create_tables():
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS authors (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            authors_id INT REFERENCES authors(id),
            available_copies INT CHECK(available_copies >= 0)
        );
        
        CREATE TABLE IF NOT EXISTS bot_users (
            telegram_id BIGINT PRIMARY KEY,
            fullname VARCHAR(100),
            joined_date DATE
        );
        '''
    )

def add_user(telegram_id, full_name):
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO bot_users(telegram_id, fullname) VALUES (%s,%s);
        ''',
        (telegram_id,full_name,)
    )

def check_user(telegram_id):
    conn = get_connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            SELECT telegram_id FROM bot_users WHERE id = %s;
            ''',
            (telegram_id,)
        )
        return True

    except Exception as e:
        return False




def get_books():
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT b.title, a.name, b.available_copies 
        FROM books b 
        JOIN authors a ON b.authors_id = a.id;
        '''
    )

    books = cursor.fetchall()

    return books

def search_book(title):
    conn = get_connect()
    cursor = conn.cursor()
    search_title = f"%{title}%"
    cursor.execute(
        '''
        SELECT title, available_copies FROM books WHERE title LIKE %s;
        ''',
        (search_title,)
    )

    return cursor.fetchall()
