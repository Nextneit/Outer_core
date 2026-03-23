import os
import copy
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk
from metadata_service import (
    ALLOWED_EXTENSIONS,
    MODIFIABLE_EXTENSIONS,
    get_basic_info,
    load_metadata_rows,
    format_exif_value,
    convert_user_value_for_exif,
    strip_metadata,
    write_jpeg_exif,
    save_png_text_metadata,
)


class ScorpionApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Scorpion - Metadata Forensics (Bonus)')
        self.root.geometry('800x600')

        self.current_filepath = None
        self.exif_dict = None
        self.tree_meta = {}

        self._setup_ui()

    def _current_extension(self):
        if not self.current_filepath:
            return None
        return os.path.splitext(self.current_filepath)[1].lower()

    def _set_edit_buttons_enabled(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.btn_clear.config(state=state)
        self.btn_save_mod.config(state=state)

    def _setup_ui(self):
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X)

        btn_open = tk.Button(top_frame, text='Open Image', command=self.open_image, bg='lightblue')
        btn_open.pack(side=tk.LEFT, padx=10)

        self.btn_clear = tk.Button(
            top_frame,
            text='Strip EXIF (Clean)',
            command=self.clear_metadata,
            state=tk.DISABLED,
            bg='#ff9999',
        )
        self.btn_clear.pack(side=tk.LEFT, padx=10)

        self.btn_save_mod = tk.Button(
            top_frame,
            text='Save Modified EXIF',
            command=self.save_edited_metadata,
            state=tk.DISABLED,
            bg='#99ff99',
        )
        self.btn_save_mod.pack(side=tk.LEFT, padx=10)

        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_paned)
        main_paned.add(left_frame, minsize=250)

        self.lbl_image = tk.Label(left_frame, text='No Image', bg='gray', width=30, height=15)
        self.lbl_image.pack(fill=tk.X, pady=5)

        self.text_basic = tk.Text(left_frame, height=8, width=30, state=tk.DISABLED)
        self.text_basic.pack(fill=tk.BOTH, expand=True, pady=5)

        right_frame = tk.Frame(main_paned)
        main_paned.add(right_frame, minsize=400)

        tree_scroll_y = tk.Scrollbar(right_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = tk.Scrollbar(right_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        columns = ('Tag', 'Value')
        self.tree = ttk.Treeview(
            right_frame,
            columns=columns,
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
        )

        style = ttk.Style()
        style.configure('Treeview', rowheight=25)

        self.tree.heading('Tag', text='Attribute (Tag)')
        self.tree.heading('Value', text='Value (Double click to edit)')
        self.tree.column('Tag', width=250, anchor=tk.W, stretch=tk.YES)
        self.tree.column('Value', width=550, anchor=tk.W, stretch=tk.YES)
        self.tree.pack(fill=tk.BOTH, expand=True)

        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        self.tree.bind('<Double-1>', self.on_double_click_tree)

    def load_basic_info(self, filepath):
        created, mod, size = get_basic_info(filepath)

        try:
            img = Image.open(filepath)
        except Exception:
            return 'Error loading basic info'

        info = f"File: {os.path.basename(filepath)}\n"
        info += f"Size: {size} bytes\n"
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
            self.tk_image = ImageTk.PhotoImage(img)
            self.lbl_image.config(image=self.tk_image, text='')
        except Exception:
            self.lbl_image.config(image='', text='Error Displaying')

    def open_image(self):
        filepath = filedialog.askopenfilename(filetypes=[('Images', '*.jpg *.jpeg *.png *.gif *.bmp')])
        if not filepath:
            return

        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            messagebox.showerror('Error', f'Unsupported extension: {ext}')
            return

        self.current_filepath = filepath
        self.display_image(filepath)

        self.text_basic.config(state=tk.NORMAL)
        self.text_basic.delete(1.0, tk.END)
        self.text_basic.insert(tk.END, self.load_basic_info(filepath))
        self.text_basic.config(state=tk.DISABLED)

        self.load_exif_to_tree(filepath)

        if ext in MODIFIABLE_EXTENSIONS:
            self._set_edit_buttons_enabled(True)
        else:
            self._set_edit_buttons_enabled(False)
            messagebox.showinfo(
                'Info',
                'Modification/Removal is currently only supported for JPEG and PNG files in this GUI.',
            )

    def load_exif_to_tree(self, filepath):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree_meta = {}

        try:
            self.exif_dict, rows = load_metadata_rows(filepath)
            for row in rows:
                iid = self.tree.insert('', tk.END, values=(row['tag'], row['value']))
                if row.get('meta'):
                    self.tree_meta[iid] = row['meta']

        except Exception as e:
            self.tree.insert('', tk.END, values=('Error reading EXIF', str(e)))

    def on_double_click_tree(self, event):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        col_id = self.tree.identify_column(event.x)
        if col_id != '#2':
            return

        current_val = self.tree.item(item, 'values')[1]

        def save_edit():
            new_val = entry_edit.get()
            vals = self.tree.item(item, 'values')
            self.tree.item(item, values=(vals[0], new_val))
            edit_win.destroy()
            messagebox.showinfo(
                'Info',
                "Value updated visually.\nDon't forget to click 'Save Modified EXIF' to write it to the image.",
            )

        edit_win = tk.Toplevel(self.root)
        edit_win.title('Edit Value')
        tk.Label(edit_win, text='New Value:').pack(pady=5)
        entry_edit = tk.Entry(edit_win, width=40)
        entry_edit.insert(0, current_val)
        entry_edit.pack(pady=5, padx=10)
        tk.Button(edit_win, text='Confirm', command=save_edit).pack(pady=5)

    def clear_metadata(self):
        if not self.current_filepath:
            return

        ext = self._current_extension()
        default_ext = '.png' if ext == '.png' else '.jpg'
        save_path = filedialog.asksaveasfilename(defaultextension=default_ext, initialfile=f'cleaned_image{default_ext}')
        if save_path:
            try:
                strip_metadata(self.current_filepath, save_path)
                messagebox.showinfo('Success', 'All EXIF/Metadata stripped successfully! Image cleaned.')
            except Exception as e:
                messagebox.showerror('Error', f'Could not clear metadata: {e}')

    def save_edited_metadata(self):
        if not self.current_filepath:
            return

        ext = self._current_extension()
        default_ext = '.png' if ext == '.png' else '.jpg'
        save_path = filedialog.asksaveasfilename(defaultextension=default_ext, initialfile=f'modified_image{default_ext}')

        if save_path:
            try:
                if ext in {'.jpg', '.jpeg'} and self.exif_dict:
                    edited_exif = copy.deepcopy(self.exif_dict)

                    for item in self.tree.get_children():
                        meta = self.tree_meta.get(item)
                        if not meta:
                            continue

                        ifd_name = meta['ifd']
                        tag_id = meta['tag_id']
                        value_type = meta['type']
                        user_value = self.tree.item(item, 'values')[1]

                        try:
                            converted = convert_user_value_for_exif(value_type, user_value)
                        except Exception as conv_error:
                            tag_label = self.tree.item(item, 'values')[0]
                            messagebox.showerror('Error', f'Invalid value for {tag_label}: {conv_error}')
                            return

                        edited_exif[ifd_name][tag_id] = converted

                    write_jpeg_exif(self.current_filepath, edited_exif, save_path)
                    messagebox.showinfo('Success', f'Metadata updated and saved to {save_path}')

                elif ext == '.png':
                    metadata_map = {}

                    for item in self.tree.get_children():
                        tag_name, val = self.tree.item(item, 'values')
                        if tag_name and tag_name != 'Error reading EXIF':
                            metadata_map[str(tag_name)] = str(val)

                    save_png_text_metadata(self.current_filepath, metadata_map, save_path)
                    messagebox.showinfo('Success', f'Metadata injected and saved to {save_path}')
            except Exception as e:
                messagebox.showerror('Error', f'Could not save modified image: {e}')


def launch_gui():
    root = tk.Tk()
    ScorpionApp(root)
    root.mainloop()
