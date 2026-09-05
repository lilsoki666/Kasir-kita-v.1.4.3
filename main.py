import os
import shutil
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import ListProperty, NumericProperty, StringProperty

import database

# Inisialisasi Database SQLite
database.init_db()

# Helper untuk menyimpan gambar produk secara aman di Android/Desktop
def save_product_image_file(source_path):
    if not source_path or not os.path.exists(source_path):
        return ""
    try:
        app = App.get_running_app()
        app_dir = app.user_data_dir if app else os.getcwd()
        images_dir = os.path.join(app_dir, 'product_images')
        
        if not os.path.exists(images_dir):
            os.makedirs(images_dir, exist_ok=True)
            
        ext = os.path.splitext(source_path)[1]
        new_filename = f"img_{int(time.time())}{ext}"
        dest_path = os.path.join(images_dir, new_filename)
        
        shutil.copy2(source_path, dest_path)
        return dest_path
    except Exception as e:
        print(f"Gagal memproses gambar: {e}")
        return source_path

KV = '''
ScreenManager:
    MainScreen:
    ProductScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        # Header Navigation
        BoxLayout:
            size_hint_y: 0.1
            spacing: 10
            Label:
                text: "UT Kasir Kita"
                font_size: '22sp'
                bold: True
            Button:
                text: "Kelola Produk"
                size_hint_x: 0.3
                on_release: app.root.current = 'product'

        # Main Layout: Produk & Keranjang
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10

            # Panel Kiri: Daftar Produk
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.6
                Label:
                    text: "Daftar Produk"
                    size_hint_y: 0.08
                    bold: True
                ScrollView:
                    GridLayout:
                        id: grid_products
                        cols: 2
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 10
                        padding: 5

            # Panel Kanan: Kasir & Keranjang
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.4
                spacing: 5

                Label:
                    text: "Keranjang Belanja"
                    size_hint_y: 0.08
                    bold: True

                ScrollView:
                    GridLayout:
                        id: grid_cart
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 5

                BoxLayout:
                    size_hint_y: 0.1
                    Label:
                        text: "Total:"
                        bold: True
                    Label:
                        id: lbl_total
                        text: "Rp 0"
                        bold: True

                BoxLayout:
                    size_hint_y: 0.12
                    spacing: 5
                    TextInput:
                        id: txt_pay
                        hint_text: "Uang Bayar"
                        input_filter: 'float'
                        multiline: False
                    Button:
                        text: "Bayar"
                        background_color: (0.2, 0.7, 0.3, 1)
                        on_release: root.process_payment()

<ProductScreen>:
    name: 'product'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout:
            size_hint_y: 0.08
            spacing: 10
            Button:
                text: "< Kembali"
                size_hint_x: 0.2
                on_release: app.root.current = 'main'
            Label:
                text: "Manajemen Produk"
                font_size: '20sp'
                bold: True

        # Form Input Produk
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.4
            spacing: 5
            
            TextInput:
                id: txt_code
                hint_text: "Kode Produk"
                multiline: False
            TextInput:
                id: txt_name
                hint_text: "Nama Produk"
                multiline: False
            TextInput:
                id: txt_price
                hint_text: "Harga Produk"
                input_filter: 'float'
                multiline: False
            TextInput:
                id: txt_stock
                hint_text: "Stok Produk"
                input_filter: 'int'
                multiline: False
            
            BoxLayout:
                spacing: 10
                Button:
                    text: "Pilih Gambar Produk"
                    on_release: root.open_file_chooser()
                Label:
                    id: lbl_image_path
                    text: "Belum ada gambar"
                    shorten: True

            BoxLayout:
                spacing: 10
                size_hint_y: 0.8
                Button:
                    text: "Simpan Produk"
                    background_color: (0.2, 0.6, 0.9, 1)
                    on_release: root.save_product()
                Button:
                    text: "Reset"
                    on_release: root.clear_form()

        # Tabel Daftar Produk
        Label:
            text: "Daftar Produk Terdaftar"
            size_hint_y: 0.05
            bold: True

        ScrollView:
            GridLayout:
                id: grid_product_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 5
'''

class MainScreen(Screen):
    cart = []
    total_amount = 0

    def on_enter(self):
        self.load_products()

    def load_products(self):
        grid = self.ids.grid_products
        grid.clear_widgets()
        products = database.get_all_products()

        for p in products:
            btn_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=5)
            
            # Tampilan Tombol Produk
            img_text = f"[{p['name']}]\nRp {p['price']:,.0f} | Stok: {p['stock']}"
            btn = Button(text=img_text, halign='center')
            btn.bind(on_release=lambda x, prod=p: self.add_to_cart(prod))
            btn_layout.add_widget(btn)
            
            grid.add_widget(btn_layout)

    def add_to_cart(self, product):
        if product['stock'] <= 0:
            self.show_popup("Peringatan", "Stok produk habis!")
            return

        # Cek apakah item sudah di keranjang
        for item in self.cart:
            if item['id'] == product['id']:
                if item['qty'] + 1 > product['stock']:
                    self.show_popup("Peringatan", "Jumlah melebihi stok tersedia!")
                    return
                item['qty'] += 1
                item['subtotal'] = item['qty'] * item['price']
                self.update_cart_ui()
                return

        self.cart.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'qty': 1,
            'subtotal': product['price']
        })
        self.update_cart_ui()

    def update_cart_ui(self):
        grid = self.ids.grid_cart
        grid.clear_widgets()
        self.total_amount = 0

        for item in self.cart:
            self.total_amount += item['subtotal']
            row = BoxLayout(size_hint_y=None, height=40, spacing=5)
            row.add_widget(Label(text=f"{item['name']} x{item['qty']}"))
            row.add_widget(Label(text=f"Rp {item['subtotal']:,.0f}"))
            
            btn_del = Button(text="X", size_hint_x=0.2, background_color=(1, 0.3, 0.3, 1))
            btn_del.bind(on_release=lambda x, i=item: self.remove_from_cart(i))
            row.add_widget(btn_del)
            
            grid.add_widget(row)

        self.ids.lbl_total.text = f"Rp {self.total_amount:,.0f}"

    def remove_from_cart(self, item):
        self.cart.remove(item)
        self.update_cart_ui()

    def process_payment(self):
        if not self.cart:
            self.show_popup("Error", "Keranjang belanja kosong!")
            return

        pay_text = self.ids.txt_pay.text
        if not pay_text:
            self.show_popup("Error", "Masukkan nominal pembayaran!")
            return

        pay = float(pay_text)
        if pay < self.total_amount:
            self.show_popup("Error", "Uang pembayaran kurang!")
            return

        change = pay - self.total_amount
        invoice = f"INV-{int(time.time())}"

        success, msg = database.save_transaction(invoice, self.total_amount, pay, change, self.cart)
        if success:
            self.show_popup("Transaksi Berhasil", f"Kembalian: Rp {change:,.0f}")
            self.cart = []
            self.ids.txt_pay.text = ""
            self.update_cart_ui()
            self.load_products()
        else:
            self.show_popup("Error", msg)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()


class ProductScreen(Screen):
    selected_image_path = ""

    def on_enter(self):
        self.load_product_list()

    def open_file_chooser(self):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path=os.getcwd(), filters=['*.png', '*.jpg', '*.jpeg'])
        content.add_widget(file_chooser)

        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        btn_select = Button(text="Pilih")
        btn_cancel = Button(text="Batal")
        btn_layout.add_widget(btn_select)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup = Popup(title="Pilih Gambar Produk", content=content, size_hint=(0.9, 0.9))

        def select_file(instance):
            if file_chooser.selection:
                self.selected_image_path = file_chooser.selection[0]
                self.ids.lbl_image_path.text = os.path.basename(self.selected_image_path)
            popup.dismiss()

        btn_select.bind(on_release=select_file)
        btn_cancel.bind(on_release=popup.dismiss)
        popup.open()

    def save_product(self):
        code = self.ids.txt_code.text.strip()
        name = self.ids.txt_name.text.strip()
        price = self.ids.txt_price.text.strip()
        stock = self.ids.txt_stock.text.strip()

        if not (code and name and price and stock):
            self.show_popup("Error", "Semua kolom input wajib diisi!")
            return

        # Proses & simpan gambar ke storage internal
        final_image_path = save_product_image_file(self.selected_image_path)

        success, msg = database.add_product(code, name, price, stock, final_image_path)
        if success:
            self.show_popup("Sukses", msg)
            self.clear_form()
            self.load_product_list()
        else:
            self.show_popup("Error", msg)

    def clear_form(self):
        self.ids.txt_code.text = ""
        self.ids.txt_name.text = ""
        self.ids.txt_price.text = ""
        self.ids.txt_stock.text = ""
        self.ids.lbl_image_path.text = "Belum ada gambar"
        self.selected_image_path = ""

    def load_product_list(self):
        grid = self.ids.grid_product_list
        grid.clear_widgets()
        products = database.get_all_products()

        for p in products:
            row = BoxLayout(size_hint_y=None, height=40, spacing=5)
            row.add_widget(Label(text=f"[{p['code']}] {p['name']}"))
            row.add_widget(Label(text=f"Rp {p['price']:,.0f} | Stok: {p['stock']}"))
            
            btn_del = Button(text="Hapus", size_hint_x=0.2, background_color=(1, 0.2, 0.2, 1))
            btn_del.bind(on_release=lambda x, pid=p['id']: self.delete_product(pid))
            row.add_widget(btn_del)
            
            grid.add_widget(row)

    def delete_product(self, product_id):
        success, msg = database.delete_product(product_id)
        if success:
            self.load_product_list()
        else:
            self.show_popup("Error", msg)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()


class KasirApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    KasirApp().run()
