import sqlite3
import os

DB_NAME = "kasir.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabel Produk
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            image_path TEXT DEFAULT ''
        )
    ''')
    
    # Tabel Transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            pay REAL NOT NULL,
            change REAL NOT NULL
        )
    ''')
    
    # Tabel Detail Transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            qty INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- OPERASI PRODUK ---
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_product(code, name, price, stock, image_path=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (code, name, price, stock, image_path) VALUES (?, ?, ?, ?, ?)",
            (code, name, float(price), int(stock), image_path)
        )
        conn.commit()
        return True, "Produk berhasil ditambahkan"
    except sqlite3.IntegrityError:
        return False, "Kode produk sudah ada!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def update_product(product_id, code, name, price, stock, image_path=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE products SET code=?, name=?, price=?, stock=?, image_path=? WHERE id=?",
            (code, name, float(price), int(stock), image_path, product_id)
        )
        conn.commit()
        return True, "Produk berhasil diperbarui"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        return True, "Produk berhasil dihapus"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

# --- OPERASI TRANSAKSI ---
def save_transaction(invoice, total, pay, change, items):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (invoice, total, pay, change) VALUES (?, ?, ?, ?)",
            (invoice, total, pay, change)
        )
        trans_id = cursor.lastrowid
        
        for item in items:
            cursor.execute(
                "INSERT INTO transaction_details (transaction_id, product_id, product_name, price, qty, subtotal) VALUES (?, ?, ?, ?, ?, ?)",
                (trans_id, item['id'], item['name'], item['price'], item['qty'], item['subtotal'])
            )
            # Kurangi stok produk
            cursor.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (item['qty'], item['id'])
            )
            
        conn.commit()
        return True, "Transaksi berhasil disimpan"
    except Exception as e:
        conn.rollback()
        return False, f"Gagal transaksi: {str(e)}"
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
