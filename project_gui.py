# ==========================================
# Product Scraper Pro - Professional GUI
# ==========================================

import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from project_scraper import ProductScraper
from project_exporter import ExcelExporter

from tkinter import ttk


# ------------------------------------------
# THEME
# ------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ------------------------------------------
# MAIN GUI
# ------------------------------------------

class ProductScraperGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Product Scraper Pro"
        )

        self.root.geometry(
            "600x550"
        )

        self.root.minsize(
            600,
            550
        )

        self.scraper = ProductScraper()

        self.exporter = ExcelExporter()

        self.products = []

        self.scraping = False

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        self.scraper.log_callback = None

        self.scraper.progress_callback = (
            lambda value:
            self.root.after(
                0,
                lambda:
                self.update_progress(value)
            )
        )

        self.scraper.product_callback = (
            lambda product:
            self.root.after(
                0,
                lambda:
                self.add_product_row(product)
            )
        )

        self.build_ui()

    def update_table(self):

        for item in self.table.get_children():
            self.table.delete(item)

        for product in self.products:

            self.table.insert(
                "",
                "end",
                values=(
                    product.get(
                        "Product Name",
                        ""
                    ),
                    product.get(
                        "Price",
                        ""
                    ),
                    product.get(
                        "Link",
                        ""
                    )
                )
            )

    def add_product_row(
        self,
        product
    ):

        print(
            "GUI RECEIVED:",
            product
        )

        self.products.append(product)

        self.table.insert(
            "",
            "end",
            values=(
                product.get(
                    "Product Name",
                    ""
                ),
                product.get(
                    "Price",
                    ""
                    ),
                product.get(
                    "Link",
                    ""
                )
            )
        )

        self.product_label.configure(
            text=f"Products Found: {len(self.table.get_children())}"
        )


    def on_close(self):

        try:
            self.scraper.stop()
        except:
            pass

        self.root.destroy()

    # ----------------------------------
    # UI
    # ----------------------------------

    def build_ui(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=28
        )

        style.configure(
            "Treeview.Heading",
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

        # HEADER

        header = ctk.CTkLabel(
            self.root,
            text="PRODUCT SCRAPER PRO",
            font=(
                "Segoe UI",
                28,
                "bold"
            )
        )

        header.pack(
            pady=10
        )

        # URL FRAME

        url_frame = ctk.CTkFrame(
            self.root
        )

        url_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ctk.CTkLabel(
            url_frame,
            text="Category URL"
        ).pack(
            anchor="w",
            padx=3,
            pady=(5, 0)
        )

        self.url_entry = ctk.CTkEntry(
            url_frame,
            height=10,
            width=500,
            placeholder_text=
            "https://example.com/category"
        )

        self.url_entry.pack(
            fill="x",
            padx=3,
            pady=5
        )

        # OPTIONS FRAME

        options = ctk.CTkFrame(
            self.root
        )

        options.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # KEYWORD
        ctk.CTkLabel(
            options,
            text="Keyword"
        ).grid(
            row=0,
            column=2,
            padx=3,
            pady=5
        )

        self.keyword_entry = ctk.CTkEntry(
            options,
            width=200
        )

        self.keyword_entry.grid(
            row=0,
            column=3,
            padx=3,
            pady=5
        )

        self.keyword_entry.insert(
            0,
            ""
        )

        ctk.CTkLabel(
            options,
            text="Max Pages"
        ).grid(
            row=0,
            column=0,
            padx=3,
            pady=5
        )

        self.pages_entry = (
            ctk.CTkEntry(
                options,
                width=120
            )
        )

        self.pages_entry.insert(
            0,
            "5"
        )

        self.pages_entry.grid(
            row=0,
            column=1,
            padx=3,
            pady=5
        )

        # BUTTONS

        btn_frame = ctk.CTkFrame(
            self.root
        )

        btn_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.start_btn = (
            ctk.CTkButton(
                btn_frame,
                text="START",
                command=
                self.start_scraping,
                width=100,
                height=25
            )
        )

        self.start_btn.pack(
            side="left",
            padx=3,
            pady=5
        )

        self.stop_btn = (
            ctk.CTkButton(
                btn_frame,
                text="STOP",
                command=
                self.stop_scraping,
                width=100,
                height=25
            )
        )

        self.stop_btn.pack(
            side="left",
            padx=3
        )

        self.export_btn = (
            ctk.CTkButton(
                btn_frame,
                text="EXPORT EXCEL",
                command=
                self.export_excel,
                width=120,
                height=25
            )
        )

        self.export_btn.pack(
            side="left",
            padx=3
        )

        self.refresh_btn = (
            ctk.CTkButton(
                btn_frame,
                text="REFRESH",
                command=self.refresh_dashboard,
                width=100,
                height=25
            )
        )

        self.refresh_btn.pack(
            side="left",
            padx=3
        )

        # STATUS

        status_frame = ctk.CTkFrame(
            self.root
        )

        status_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.product_label = ctk.CTkLabel(
            status_frame,
            text="Products Found: 0",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        )

        self.product_label.pack(
            side="left",
            padx=10,
            pady=5
        )

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="READY",
            text_color="white",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        )

        self.status_label.pack(
            side="right",
            padx=10,
            pady=5
        )

        # PROGRESS

        self.progress_bar = (
            ctk.CTkProgressBar(
                self.root,
                height=10
            )
        )

        self.progress_bar.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.progress_bar.set(
            0
        )

        # ==============
        # PRODUCT TABLE
        # ==============
        table_frame = ctk.CTkFrame(
            self.root
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "name",
            "price",
            "link"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=4
        )

        self.table.heading(
            "name",
            text="Product Name"
        )

        self.table.heading(
            "price",
            text="Price"
        )

        self.table.heading(
            "link",
            text="Link"
        )

        self.table.column(
            "name",
            width=350
        )

        self.table.column(
            "price",
            width=120
        )

        self.table.column(
            "link",
            width=350,
            stretch=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=
            scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )
        

    # ----------------------------------
    # PROGRESS
    # ----------------------------------

    def update_progress(
        self,
        value
    ):

        self.progress_bar.set(
            value
        )

        self.root.update_idletasks()

    # ----------------------------------
    # START
    # ----------------------------------

    def start_scraping(self):

        if self.scraping:
            return

        self.scraping = True

        url = (
            self.url_entry
            .get()
            .strip()
        )

        keyword = (
            self.keyword_entry
            .get()
            .strip()
        )

        if not url.startswith(
            ("http://", "https://")
        ):
            self.scraping = False

            messagebox.showerror(
                "Error",
                "Enter valid URL"
            )

            return

        try:

            max_pages = int(
                self.pages_entry.get()
            )

            # ===== PAGE VALIDATION =====
            if max_pages < 1:

                self.scraping = False

                messagebox.showerror(
                    "Error",
                    "Page count must be greater than 0"
                )

                return

        except:

            self.scraping = False

            messagebox.showerror(
                "Error",
                "Invalid page count"
            )

            return

        self.products = []

        for item in self.table.get_children():
            self.table.delete(item)

        self.product_label.configure(
            text="Products Found: 0"
        )

        self.progress_bar.set(
            0
        )

        self.status_label.configure(
            text="SCRAPER SEARCHING...",
            text_color="red"
        )

        threading.Thread(
            target=
            self.run_scraper,
            args=(
                url,
                max_pages,
                keyword
            ),
            daemon=True
        ).start()

    # ----------------------------------
    # SCRAPER THREAD
    # ----------------------------------

    def run_scraper(
        self,
        url,
        max_pages,
        keyword
    ):

        try:

            self.products = (
                self.scraper.scrape(
                    url,
                    max_pages,
                    keyword
                )
            )

            self.root.after(
                0,
                lambda: self.product_label.configure(
                    text=f"Products Found: {len(self.products)}"
                )
            )

        except Exception as e:

            error_msg = str(e)

            self.root.after(
                0,
                lambda: self.status_label.configure(
                    text="SCRAPER COMPLETE",
                    text_color="green"
                )
            )

        finally:

            self.scraping = False

    # ----------------------------------
    # STOP
    # ----------------------------------

    def stop_scraping(self):

        self.scraper.stop()

        self.status_label.configure(
            text="STOPPED",
            text_color="orange"
        )

    # ------------------
    # REFRESH DASHBOARD
    # ------------------
    def refresh_dashboard(self):

        try:

            self.scraper.stop()

        except:
            pass

        self.products.clear()

        self.scraping = False

        self.url_entry.delete(
            0,
            "end"
        )

        self.pages_entry.delete(
            0,
            "end"
        )

        self.pages_entry.insert(
            0,
            "5"
        )

        for item in self.table.get_children():

            self.table.delete(item)

        self.product_label.configure(
            text="Products Found: 0"
        )

        self.progress_bar.set(
            0
        )

        self.status_label.configure(
            text="READY",
            text_color="white"
        )

    # ----------------------------------
    # EXPORT
    # ----------------------------------

    def export_excel(self):

        if not self.products:

            messagebox.showwarning(
                "Warning",
                "No data available"
            )

            return

        save_file = (
            filedialog
            .asksaveasfilename(
                defaultextension=
                ".xlsx",
                filetypes=[
                    (
                        "Excel",
                        "*.xlsx"
                    )
                ]
            )
        )

        if not save_file:
            return

        try:

            self.exporter.save_products(
                self.products,
                save_file
            )

            messagebox.showinfo(
                "Success",
                "Excel Saved"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )
