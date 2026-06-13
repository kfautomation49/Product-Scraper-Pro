# ====================
# Product Scraper Pro
# Main Launcher
# ====================

import os
import sys

import customtkinter as ctk

from project_gui import ProductScraperGUI

def main():

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    try:

        root.iconbitmap(
            resource_path(
                "scraper_logo.ico"
            )
        )

    except:
        pass

    root.title("Product Scraper Pro")

    root.geometry("600x550")
    root.resizable(
        True,
        True
    )

    app = ProductScraperGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
