import tkinter as tk
from tkinter import messagebox
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
    
    main_window = tk.Tk()
    main_window.title("Quản lý Sản phẩm")

    # Form để thêm sản phẩm
    tk.Label(main_window, text="Tên sản phẩm:").pack()
    new_name_entry = tk.Entry(main_window)
    new_name_entry.pack()

    tk.Label(main_window, text="Mô tả sản phẩm:").pack()
    new_description_entry = tk.Entry(main_window)
    new_description_entry.pack()

    tk.Label(main_window, text="Giá sản phẩm:").pack()
    new_price_entry = tk.Entry(main_window)
    new_price_entry.pack()

    tk.Button(main_window, text="Thêm sản phẩm", command=add_product).pack()

    # Text box để hiển thị danh sách sản phẩm
    result_text = tk.Text(main_window, height=10, width=50)
    result_text.pack()

    tk.Button(main_window, text="Xem sản phẩm", command=view_products).pack()

    main_window.mainloop()

# Hàm để thêm sản phẩm
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

# Hàm để hiển thị danh sách sản phẩm
def view_products():
    products = database.get_all_products(conn)
    
    result_text.delete(1.0, tk.END)  # Xóa nội dung trước
    for product in products:
        result_text.insert(tk.END, f"ID: {product[0]}, Tên: {product[1]}, Mô tả: {product[2]}, Giá: {product[3]}\n")

# Cửa sổ đăng nhập
login_window = tk.Tk()
login_window.title("Đăng nhập")

tk.Label(login_window, text="Username:").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password:").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Đăng nhập", command=login).pack()

login_window.mainloop()
