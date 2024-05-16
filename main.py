import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, ttk
import os
import fitz  # Importe PyMuPDF
from PIL import Image, ImageTk  # Importe Pillow et ImageTk pour le traitement des images
from datetime import datetime

def update_pdf_count(*args):
    folder = folder_path.get()
    if folder and os.path.isdir(folder):
        num_pdfs = sum(1 for f in os.listdir(folder) if f.lower().endswith('.pdf'))
        pdf_count.set(f"Nombre de PDFs dans le dossier: {num_pdfs}")
    else:
        pdf_count.set("Nombre de PDFs dans le dossier: 0")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def convert_pdf_to_tiff(pdf_path, output_folder):
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            zoom_x = 600 / 72  # 600 DPI for X axis
            zoom_y = 600 / 72  # 600 DPI for Y axis
            mat = fitz.Matrix(zoom_x, zoom_y)  # Define the transformation matrix for zoom
            pix = page.get_pixmap(matrix=mat)
            img_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page{page_num + 1}.png")
            pix.save(img_path)
            img = Image.open(img_path)
            tiff_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page{page_num + 1}.tiff")
            img.save(tiff_path, 'TIFF')
            os.remove(img_path)
        doc.close()
        return True
    except Exception as e:
        return e

def start_conversion(selected_files=None):
    folder = folder_path.get()
    num_files_converted = 0
    if not folder:
        messagebox.showerror("Erreur", "Veuillez sélectionner un dossier.")
        return
    if not os.listdir(folder):
        messagebox.showerror("Erreur", "Le dossier est vide.")
        return

    errors = []
    files_to_convert = selected_files if selected_files else [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]

    for filename in files_to_convert:
        pdf_path = os.path.join(folder, filename)
        result = convert_pdf_to_tiff(pdf_path, folder)
        if result is True:
            num_files_converted += 1
        else:
            errors.append(f"Erreur avec le fichier {filename}: {result}")

    if not errors:
        messagebox.showinfo("Succès", f"Les {num_files_converted} fichiers ont bien été convertis.")
    else:
        messagebox.showerror("Erreur", "\n".join(errors))

def open_file_selection_window():
    selection_window = Toplevel(root)
    selection_window.title("Sélectionner les fichiers PDF")
    selection_window.geometry("600x400")

    tree = ttk.Treeview(selection_window, columns=("name", "mod_time", "size"), show='headings')
    tree.heading("name", text="Nom du fichier")
    tree.heading("mod_time", text="Date de modification")
    tree.heading("size", text="Taille")
    tree.column("name", width=250)
    tree.column("mod_time", width=150)
    tree.column("size", width=100)

    folder = folder_path.get()
    files_info = []
    if folder and os.path.isdir(folder):
        pdf_files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
        for pdf in pdf_files:
            file_path = os.path.join(folder, pdf)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')
            size = os.path.getsize(file_path)
            size_str = f"{size / 1024:.2f} KB"
            files_info.append((pdf, mod_time, size_str))

    for file_info in files_info:
        tree.insert("", "end", values=file_info)

    tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

    def select_all():
        for item in tree.get_children():
            tree.selection_add(item)

    def deselect_all():
        for item in tree.get_children():
            tree.selection_remove(item)

    def start_conversion_with_selection():
        selected_items = tree.selection()
        selected_files = [tree.item(item, "values")[0] for item in selected_items]
        selection_window.destroy()
        start_conversion(selected_files)

    button_frame = tk.Frame(selection_window)
    button_frame.pack(fill=tk.X, pady=10)

    select_all_button = tk.Button(button_frame, text="Tout sélectionner", command=select_all, width=20)
    select_all_button.pack(side=tk.LEFT, padx=10)

    deselect_all_button = tk.Button(button_frame, text="Tout déselectionner", command=deselect_all, width=20)
    deselect_all_button.pack(side=tk.LEFT, padx=10)

    convert_button = tk.Button(button_frame, text="Convertir les fichiers sélectionnés", command=start_conversion_with_selection, width=20)
    convert_button.pack(side=tk.RIGHT, padx=10)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Conversion de PDF vers TIFF")
root.geometry("600x400")  # Définit la taille de la fenêtre

# Chargement et affichage du logo
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=10)  # Centré automatiquement

# Séparateur
separator1 = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator1.pack(fill=tk.X, padx=150, pady=5)

# Variables globales
folder_path = tk.StringVar()
pdf_count = tk.StringVar(value="Nombre de PDFs dans le dossier: 0")
folder_path.trace("w", update_pdf_count)  # Ajout de la fonction de traçage

# Interface
path_label = tk.Label(root, text="Chemin du dossier:")
path_label.pack()
path_entry = tk.Entry(root, textvariable=folder_path, width=50)
path_entry.pack(pady=5)
browse_button = tk.Button(root, text="Parcourir", command=browse_folder, width=20)
browse_button.pack(pady=5)
pdf_count_label = tk.Label(root, textvariable=pdf_count)
pdf_count_label.pack(pady=10)

# Bouton pour ouvrir la nouvelle fenêtre de sélection de fichiers
select_files_button = tk.Button(root, text="Sélectionner les fichiers PDF", command=open_file_selection_window, width=20)
select_files_button.pack(pady=5)

# Séparateur
separator2 = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator2.pack(fill=tk.X, padx=150, pady=5)

start_button = tk.Button(root, text="Lancer la conversion", command=lambda: start_conversion(), width=20)
start_button.pack(pady=20)

# Lancement de l'application
root.mainloop()
