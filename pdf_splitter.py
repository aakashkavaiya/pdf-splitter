import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedTk

def get_file_paths(entry_files):
    file_paths = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF Files", "*.pdf")])

    if file_paths:
        entry_files.delete(0, tk.END)
        entry_files.insert(0, ";".join(file_paths))

def merge_pdfs(file_list, output_path, status_label):
    pdf_writer = fitz.open()

    for file_path in file_list.split(";"):
        pdf_document = fitz.open(file_path)
        pdf_writer.insert_pdf(pdf_document)
        pdf_document.close()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_filename = os.path.join(output_path, "merged_output.pdf")
    pdf_writer.save(output_filename)
    pdf_writer.close()

    status_label.config(text="Merging successful!", fg="green")

def reset_fields(entry_files, status_label):
    entry_files.delete(0, tk.END)
    status_label.config(text="")

def create_pdf_merger_gui():
    root = ThemedTk(theme="equilux")  # Choose a theme (e.g., "equilux")
    root.title("PDF Merger")
    root.geometry("600x300")  # Increase window size

    label_title = tk.Label(root, text="PDF Merger", font=("Helvetica", 20))
    label_title.pack(pady=10)

    label_maker = tk.Label(root, text="by Your Name", font=("Helvetica", 12))
    label_maker.pack(pady=5)

    entry_files = tk.Entry(root, width=50)
    entry_files.pack(pady=5, padx=10)

    btn_browse_files = tk.Button(root, text="Browse", command=lambda: get_file_paths(entry_files))
    btn_browse_files.pack(pady=5)

    output_var = tk.StringVar()
    entry_output = tk.Entry(root, textvariable=output_var, width=50)
    entry_output.pack(pady=5, padx=10)

    btn_browse_output = tk.Button(root, text="Select Output Folder", command=lambda: get_output_path(output_var))
    btn_browse_output.pack(pady=5)

    btn_merge = tk.Button(root, text="Merge PDFs", command=lambda: merge_pdfs(entry_files.get(), output_var.get(), status_label))
    btn_merge.pack(pady=10)

    btn_reset = tk.Button(root, text="Reset", command=lambda: reset_fields(entry_files, status_label))
    btn_reset.pack(pady=5)

    status_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red")
    status_label.pack(pady=5)

    root.mainloop()

def get_output_path(entry_var):
    output_path = filedialog.askdirectory(title="Select Output Folder")

    if output_path:
        entry_var.set(output_path)

if __name__ == "__main__":
    create_pdf_merger_gui()
