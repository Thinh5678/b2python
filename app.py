import tkinter as tk
from tkinter import ttk, messagebox
import database

# Cửa sổ đăng nhập
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    global conn
    conn = database.connect_db(username, password)
    
    if conn:
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Thất bại", "Đăng nhập thất bại. Vui lòng thử lại.")

# Cửa sổ chính để xem và thêm sản phẩm
def open_main_window():
    global new_name_entry, new_description_entry, new_price_entry, result_text
    global product_id_entry, update_name_entry, update_description_entry, update_price_entry
    
    main_window = tk.Tk()
    main_window.title("Quản lý Sản phẩm")

    # Frame Thêm sản phẩm
    add_frame = ttk.LabelFrame(main_window, text="Thêm sản phẩm", padding=10)
    add_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(add_frame, text="Tên sản phẩm:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    new_name_entry = ttk.Entry(add_frame)
    new_name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(add_frame, text="Mô tả sản phẩm:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    new_description_entry = ttk.Entry(add_frame)
    new_description_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(add_frame, text="Giá sản phẩm:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    new_price_entry = ttk.Entry(add_frame)
    new_price_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(add_frame, text="Thêm sản phẩm", command=add_product).grid(row=3, column=0, columnspan=2, pady=10)

    # Text box hiển thị danh sách sản phẩm
    result_frame = ttk.LabelFrame(main_window, text="Danh sách sản phẩm", padding=10)
    result_frame.pack(fill="x", padx=10, pady=5)

    result_text = tk.Text(result_frame, height=10, width=50)
    result_text.pack(padx=5, pady=5)

    ttk.Button(result_frame, text="Xem sản phẩm", command=view_products).pack(pady=5)

    # Frame Tìm kiếm sản phẩm
    search_frame = ttk.LabelFrame(main_window, text="Tìm kiếm sản phẩm", padding=10)
    search_frame.pack(fill="x", padx=10, pady=5)

    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5)
    ttk.Button(search_frame, text="Tìm kiếm", command=lambda: search_product(search_entry.get())).pack(side="left", padx=5)

    # Frame Cập nhật sản phẩm
    update_frame = ttk.LabelFrame(main_window, text="Cập nhật sản phẩm", padding=10)
    update_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(update_frame, text="ID sản phẩm cần sửa:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    product_id_entry = ttk.Entry(update_frame)
    product_id_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(update_frame, text="Tên mới:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    update_name_entry = ttk.Entry(update_frame)
    update_name_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(update_frame, text="Mô tả mới:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    update_description_entry = ttk.Entry(update_frame)
    update_description_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(update_frame, text="Giá mới:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    update_price_entry = ttk.Entry(update_frame)
    update_price_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(update_frame, text="Cập nhật sản phẩm", command=update_product).grid(row=4, column=0, columnspan=2, pady=10)

    # Frame Xóa sản phẩm
    delete_frame = ttk.LabelFrame(main_window, text="Xóa sản phẩm", padding=10)
    delete_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(delete_frame, text="ID sản phẩm cần xóa:").pack(side="left", padx=5)
    delete_id_entry = ttk.Entry(delete_frame)
    delete_id_entry.pack(side="left", fill="x", expand=True, padx=5)
    ttk.Button(delete_frame, text="Xóa sản phẩm", command=lambda: delete_product(delete_id_entry.get())).pack(side="left", padx=5)

    main_window.mainloop()

# Hàm thêm sản phẩm
def add_product():
    name = new_name_entry.get()
    description = new_description_entry.get()
    price = new_price_entry.get()

    if not name or not price:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin.")
        return
    
    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("Lỗi", "Giá sản phẩm phải là số.")
        return

    database.add_product(conn, name, description, price)
    messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
    view_products()

# Hàm hiển thị danh sách sản phẩm
def view_products():
    products = database.get_all_products(conn)
    result_text.delete(1.0, tk.END)
    for product in products:
        result_text.insert(tk.END, f"ID: {product[0]}, Tên: {product[1]}, Mô tả: {product[2]}, Giá: {product[3]}\n")

# Hàm tìm kiếm sản phẩm
def search_product(keyword):
    if not keyword:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm.")
        return
    
    products = database.search_products(conn, keyword)
    result_text.delete(1.0, tk.END)
    if not products:
        result_text.insert(tk.END, "Không tìm thấy sản phẩm nào.")
    else:
        for product in products:
            result_text.insert(tk.END, f"ID: {product[0]}, Tên: {product[1]}, Mô tả: {product[2]}, Giá: {product[3]}\n")

# Hàm cập nhật sản phẩm
def update_product():
    product_id = product_id_entry.get()
    name = update_name_entry.get()
    description = update_description_entry.get()
    price = update_price_entry.get()

    if not product_id or not name or not price:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin.")
        return
    
    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("Lỗi", "Giá sản phẩm phải là số.")
        return

    database.update_product(conn, product_id, name, description, price)
    messagebox.showinfo("Thành công", "Cập nhật sản phẩm thành công!")
    view_products()

# Hàm xóa sản phẩm
def delete_product(product_id):
    if not product_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID sản phẩm.")
        return

    database.delete_product(conn, product_id)
    messagebox.showinfo("Thành công", "Xóa sản phẩm thành công!")
    view_products()

# Cửa sổ đăng nhập
login_window = tk.Tk()
login_window.title("Đăng nhập")

frame = ttk.Frame(login_window, padding=10)
frame.pack(padx=10, pady=10)

ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
username_entry = ttk.Entry(frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
password_entry = ttk.Entry(frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(frame, text="Đăng nhập", command=login).grid(row=2, column=0, columnspan=2, pady=10)

login_window.mainloop()
