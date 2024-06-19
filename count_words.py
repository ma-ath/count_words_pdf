import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from tika import parser

def pdf_to_string(file_path: Path):
    try:
        text = parser.from_file(str(file_path.absolute()))['content']
        assert(text is not None)
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def save_string_to_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        directory_label.config(text=f"Selected directory: {selected_directory}")

def count_word():
    if not selected_directory:
        messagebox.showwarning("Directory Not Selected", "Please select a directory first.")
        return
    
    word = word_entry.get()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word to count.")
        return
    
    try:
        all_pdf_text = []
        print("Reading files...")
        for file_path in Path(selected_directory).glob('*.pdf'):
            all_pdf_text.append(pdf_to_string(file_path))

        print(f"Read {len(all_pdf_text)} files")
        all_pdf_text = '\n'.join(all_pdf_text)

        save_string_to_file(all_pdf_text, "ALL_FILES.txt")

        # Count number of words
        number_of_occurences = all_pdf_text.lower().count(word.lower())
        result_label.config(text=f"The word '{word}' appears {number_of_occurences} times.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the GUI
root = tk.Tk()
root.title("PDF Word Counter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

word_label = tk.Label(frame, text="Enter word to count:")
word_label.grid(row=0, column=0, padx=5, pady=5)

word_entry = tk.Entry(frame)
word_entry.grid(row=0, column=1, padx=5, pady=5)

select_button = tk.Button(frame, text="Select Directory", command=select_directory)
select_button.grid(row=1, column=0, pady=10)

count_button = tk.Button(frame, text="Count Word", command=count_word)
count_button.grid(row=1, column=1, pady=10)

directory_label = tk.Label(frame, text="No directory selected.")
directory_label.grid(row=2, column=0, columnspan=2, pady=5)

result_label = tk.Label(frame, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
