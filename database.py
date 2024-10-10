import psycopg2

# Hàm kết nối đến PostgreSQL
def connect_db(username, password):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="product_db",
            user=username,
            password=password
        )
        return conn
    except Exception as e:
        print(f"Kết nối thất bại: {e}")
        return None

# Hàm lấy tất cả sản phẩm
def get_all_products(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    cur.close()
    return products

# Hàm thêm sản phẩm mới
def add_product(conn, name, description, price):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO product (name, description, price) VALUES (%s, %s, %s)",
        (name, description, price)
    )
    conn.commit()
    cur.close()
