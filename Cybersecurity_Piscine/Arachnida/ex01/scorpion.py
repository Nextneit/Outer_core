import os
import sys
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
from PIL.PngImagePlugin import PngInfo
import piexif

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

def get_basic_info(filepath):
    stat = os.stat(filepath)
    created = datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    size = stat.st_size
    return created, modified, size

def extract_exif(filepath):
    try:
        img = Image.open(filepath)
    except Exception as e:
        print(f"Error opening file: {e}")
        return
    
    created, modified, size = get_basic_info(filepath)
    print(f"  Format      : {img.format}")
    print(f"  Mode        : {img.mode}")
    print(f"  Size        : {img.size[0]}x{img.size[1]} px")
    print(f"  File size   : {size} bytes")
    print(f"  Created     : {created}")
    print(f"  Modified    : {modified}")
    
    exif_data = img._getexif() if hasattr(img, '_getexif') else None
    
    # Intento buscar info específica de formato PNG si no hay EXIF JPEG estándar
    png_info = img.info if img.format == 'PNG' and img.info else None
    
    if exif_data:
        print("--- EXIF DATA ---")
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            print(f"{tag:<30}: {value}")
    elif png_info:
        print("--- PNG INFO/METADATA ---")
        for key, value in png_info.items():
            # Excluir parámetros de imagen básicos crudos si lo deseamos
            if key not in ['dpi', 'icc_profile', 'vpi']:
                print(f"{key:<30}: {value}")
    else:
        print("No EXIF/Metadata found")

class ScorpionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scorpion - Metadata Forensics (Bonus)")
        self.root.geometry("800x600")
        
        self.current_filepath = None
        self.exif_dict = None
        
        self._setup_ui()

    def _setup_ui(self):
        # Panel superior (Botones)
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X)

        btn_open = tk.Button(top_frame, text="Open Image", command=self.open_image, bg="lightblue")
        btn_open.pack(side=tk.LEFT, padx=10)

        self.btn_clear = tk.Button(top_frame, text="Strip EXIF (Clean)", command=self.clear_metadata, state=tk.DISABLED, bg="#ff9999")
        self.btn_clear.pack(side=tk.LEFT, padx=10)
        
        self.btn_save_mod = tk.Button(top_frame, text="Save Modified EXIF", command=self.save_edited_metadata, state=tk.DISABLED, bg="#99ff99")
        self.btn_save_mod.pack(side=tk.LEFT, padx=10)

        # Contenedor central dividido
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel izquierdo (Imagen e info básica)
        left_frame = tk.Frame(main_paned)
        main_paned.add(left_frame, minsize=250)

        self.lbl_image = tk.Label(left_frame, text="No Image", bg="gray", width=30, height=15)
        self.lbl_image.pack(fill=tk.X, pady=5)

        self.text_basic = tk.Text(left_frame, height=8, width=30, state=tk.DISABLED)
        self.text_basic.pack(fill=tk.BOTH, expand=True, pady=5)

        # Panel derecho (Tabla Editable EXIF) y barra de desplazamiento
        right_frame = tk.Frame(main_paned)
        main_paned.add(right_frame, minsize=400)

        # Configurar un Treeview con Scrollbar para que los datos no queden aplastados
        tree_scroll_y = tk.Scrollbar(right_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = tk.Scrollbar(right_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        columns = ("Tag", "Value")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", 
                                yscrollcommand=tree_scroll_y.set, 
                                xscrollcommand=tree_scroll_x.set)
        
        # Ajustar el alto de las filas para que la fuente de Linux quepa bien
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        
        self.tree.heading("Tag", text="Attribute (Tag)")
        self.tree.heading("Value", text="Value (Double click to edit)")
        
        # Las columnas deben poder estirarse
        self.tree.column("Tag", width=250, anchor=tk.W, stretch=tk.YES)
        self.tree.column("Value", width=550, anchor=tk.W, stretch=tk.YES)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        self.tree.bind("<Double-1>", self.on_double_click_tree)

    def load_basic_info(self, filepath):
        stat = os.stat(filepath)
        created = datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        mod = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            img = Image.open(filepath)
        except Exception:
            return "Error loading basic info"

        info = f"File: {os.path.basename(filepath)}\n"
        info += f"Size: {stat.st_size} bytes\n"
        info += f"Format: {img.format}\n"
        info += f"Mode: {img.mode}\n"
        info += f"Dim: {img.size[0]}x{img.size[1]} px\n"
        info += f"Created: {created}\n"
        info += f"Modified: {mod}\n"
        return info

    def display_image(self, filepath):
        try:
            img = Image.open(filepath)
            img.thumbnail((250, 250))
            self.tk_image = ImageTk.PhotoImage(img) # Guardar ref para evitar recolección de basura
            self.lbl_image.config(image=self.tk_image, text="")
        except Exception:
            self.lbl_image.config(image='', text="Error Displaying")

    def open_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if not filepath:
            return
            
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            messagebox.showerror("Error", f"Unsupported extension: {ext}")
            return

        self.current_filepath = filepath
        
        # UI Básica
        self.display_image(filepath)
        
        self.text_basic.config(state=tk.NORMAL)
        self.text_basic.delete(1.0, tk.END)
        self.text_basic.insert(tk.END, self.load_basic_info(filepath))
        self.text_basic.config(state=tk.DISABLED)

        # UI Exif
        self.load_exif_to_tree(filepath)
        
        # Habilitar funcionalidades tanto para JPEG como para PNG
        if ext in {'.jpg', '.jpeg', '.png'}:
            self.btn_clear.config(state=tk.NORMAL)
            self.btn_save_mod.config(state=tk.NORMAL)
        else:
            self.btn_clear.config(state=tk.DISABLED)
            self.btn_save_mod.config(state=tk.DISABLED)
            messagebox.showinfo("Info", "Modification/Removal is currently only supported for JPEG and PNG files in this GUI.")

    def load_exif_to_tree(self, filepath):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Intentar cargar raw dict con piexif para edición. Puede fallar en PNG.
            try:
                self.exif_dict = piexif.load(filepath)
            except Exception:
                self.exif_dict = None

            # Usar Pillow para lectura bonita 
            img = Image.open(filepath)
            exif_data = img._getexif() if hasattr(img, '_getexif') else None
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    # Convertir bytes crudos a string legible si es necesario
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = "<Binary Data>"
                    self.tree.insert("", tk.END, values=(tag_name, str(value)), tags=(tag_id,))
            elif img.format == 'PNG' and img.info:
                for key, value in img.info.items():
                    if key not in ['dpi', 'icc_profile', 'vpi']:
                        self.tree.insert("", tk.END, values=(key, str(value)), tags=(key,))
            else:
                self.tree.insert("", tk.END, values=("No EXIF data", "found"))
                
        except Exception as e:
            self.tree.insert("", tk.END, values=("Error reading EXIF", str(e)))

    def on_double_click_tree(self, event):
        item = self.tree.selection()[0]
        col_id = self.tree.identify_column(event.x)
        if col_id != "#2": # Solo permitir editar la columna de Valores
            return
            
        current_val = self.tree.item(item, "values")[1]
        
        # Crear ventana simple emergente de dialogo text
        def save_edit():
            new_val = entry_edit.get()
            # Guardamos el cambio visual
            vals = self.tree.item(item, "values")
            self.tree.item(item, values=(vals[0], new_val))
            edit_win.destroy()
            messagebox.showinfo("Info", f"Valor cambiado visualmente.\nNo olvides pulsar 'Save Modified EXIF' para inyectarlo en la imagen.")

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Value")
        tk.Label(edit_win, text="New Value:").pack(pady=5)
        entry_edit = tk.Entry(edit_win, width=40)
        entry_edit.insert(0, current_val)
        entry_edit.pack(pady=5, padx=10)
        tk.Button(edit_win, text="Confirm", command=save_edit).pack(pady=5)

    def clear_metadata(self):
        if not self.current_filepath: return
        ext = os.path.splitext(self.current_filepath)[1].lower()
        
        default_ext = ".png" if ext == ".png" else ".jpg"
        save_path = filedialog.asksaveasfilename(defaultextension=default_ext, initialfile=f"cleaned_image{default_ext}")
        if save_path:
            try:
                if ext in {'.jpg', '.jpeg'}:
                    piexif.remove(self.current_filepath, save_path)
                elif ext == '.png':
                    # Limpieza nativa de PNG usando Pillow
                    img = Image.open(self.current_filepath)
                    data = list(img.getdata()) # Fuerza carga completa purificando chunks
                    img_clean = Image.new(img.mode, img.size)
                    img_clean.putdata(data)
                    img_clean.save(save_path, "PNG")
                    
                messagebox.showinfo("Success", "All EXIF/Metadata stripped successfully! Image cleaned.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clear metadata: {e}")

    def save_edited_metadata(self):
        if not self.current_filepath: return
        ext = os.path.splitext(self.current_filepath)[1].lower()
        
        default_ext = ".png" if ext == ".png" else ".jpg"
        save_path = filedialog.asksaveasfilename(defaultextension=default_ext, initialfile=f"modified_image{default_ext}")
        
        if save_path:
            try:
                if ext in {'.jpg', '.jpeg'} and self.exif_dict:
                    # Serializar y guardar para JPEG no está implementado al 100% en esta plantilla visual
                    # Se rqueriría parsear todo el treeview. Lo dejamos bloqueado o WIP.
                    messagebox.showinfo("WIP", "JPEG specific byte-level treeview modding is a work in progress.")
                elif ext == '.png':
                    # Tomar todas las claves y valores del Treeview e inyectarlas al PNG
                    img = Image.open(self.current_filepath)
                    meta = PngInfo()
                    
                    for item in self.tree.get_children():
                        tag_name, val = self.tree.item(item, "values")
                        # PngInfo espera texto puro, ignoramos campos ilegibles o binarios
                        if tag_name and tag_name != "Error reading EXIF":
                            meta.add_text(str(tag_name), str(val))
                    
                    img.save(save_path, "PNG", pnginfo=meta)
                    messagebox.showinfo("Success", f"Metadata injected and saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save modified image: {e}")
    
def main():
    if len(sys.argv) < 2:
        root = tk.Tk()
        app = ScorpionApp(root)
        root.mainloop()
    else:
        for filepath in sys.argv[1:]:
            print(f"\n[{filepath}]")
            ext = os.path.splitext(filepath)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                print(f"  Unsupported extension: {ext}")
                continue
            if not os.path.isfile(filepath):
                print(f"  File not found.")
                continue
            extract_exif(filepath)

if __name__ == '__main__':
    main()