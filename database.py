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

# Hàm cập nhật sản phẩm
def update_product(conn, product_id, name, description, price):
    cur = conn.cursor()
    cur.execute(
        "UPDATE product SET name = %s, description = %s, price = %s WHERE id = %s",
        (name, description, price, product_id)
    )
    conn.commit()
    cur.close()

# Truy vấn sản phẩm theo từ khóa
def search_products(conn, keyword):
    cursor = conn.cursor()
    query = """
        SELECT * FROM product
        WHERE name ILIKE %s OR description ILIKE %s
    """
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    return cursor.fetchall()

# Hàm xóa sản phẩm
def delete_product(conn, product_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM product WHERE id = %s", (product_id,))
    conn.commit()
    cur.close()
