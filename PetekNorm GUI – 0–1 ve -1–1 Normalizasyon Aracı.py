import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import pandas as pd

def petek_katman_normalizasyon(data, normalize_type="0-1"):
    flat = data.flatten()
    n = len(flat)

    layers = []
    idx = 0
    layer_no = 0
    while idx < n:
        cnt = 1 if layer_no == 0 else layer_no * 6
        layers.append(flat[idx:idx+cnt])
        idx += cnt
        layer_no += 1

    normalized = []
    for layer in layers:
        arr = np.array(layer, dtype=float)
        if arr.size == 0: continue
        mn, mx = arr.min(), arr.max()
        span = mx - mn + 1e-8
        if normalize_type == "0-1":
            norm = (arr - mn) / span
        else:
            norm = 2 * (arr - mn) / span - 1
        normalized.extend(norm)
    return np.array(normalized)


class PetekNormApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        master.title("PetekNorm Normalizasyon")
        master.geometry("800x600")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=0)

        self.df_full = None
        self.raw_array = None
        self.normalized_array = None

        self.grid(sticky="nsew")

        # Treeview for Data Preview
        preview_frame = ttk.Frame(self)
        preview_frame.grid(row=0, column=0, sticky="nsew")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(preview_frame, show="headings")
        vsb = ttk.Scrollbar(preview_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Sabit Kontroller Frame (Alt kısımda)
        self.toolbar = ttk.Frame(self)
        self.toolbar.grid(row=1, column=0, sticky="ew", pady=(10, 10))

        # Dosya yükleme, normalizasyon türü ve butonlar
        ttk.Button(self.toolbar, text="Dosya Yükle", command=self.load_file).grid(row=0, column=0, padx=5)
        self.norm_type = tk.StringVar(value="0-1")
        ttk.Label(self.toolbar, text="Normalizasyon:").grid(row=0, column=1, sticky="e")
        ttk.Radiobutton(self.toolbar, text="0–1", variable=self.norm_type, value="0-1").grid(row=0, column=2)
        ttk.Radiobutton(self.toolbar, text="-1–1", variable=self.norm_type, value="-1-1").grid(row=0, column=3)
        ttk.Button(self.toolbar, text="Uygula", command=self.normalize_data).grid(row=0, column=4, padx=5)
        ttk.Button(self.toolbar, text="Kaydet", command=self.save_data).grid(row=0, column=5, padx=5)

        # Durum çubuğu
        self.status = ttk.Label(self, relief="sunken", anchor="w", padding=5)
        self.status.grid(row=2, column=0, sticky="ew")

    def set_status(self, msg, fg="black"):
        self.status.config(text=msg, foreground=fg)

    def clear_tree(self):
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        self.tree.delete(*self.tree.get_children())

    def load_file(self):
        fp = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx;*.xls"), ("CSV", "*.csv")])
        if not fp: return
        try:
            df = pd.read_csv(fp) if fp.lower().endswith(".csv") else pd.read_excel(fp)
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılamadı:\n{e}")
            return

        self.df_full = df
        num_df = df.select_dtypes(include=[np.number])
        if num_df.empty:
            messagebox.showerror("Hata", "Sayısal sütun bulunamadı.")
            return
        self.raw_array = num_df.values
        self.display_dataframe(df)
        self.set_status("Dosya yüklendi. Hazır.", "green")

    def display_dataframe(self, df):
        self.clear_tree()
        cols = list(df.columns)
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor="center")
        for _, row in df.head(100).iterrows():
            self.tree.insert("", "end", values=list(row))

    def normalize_data(self):
        if self.raw_array is None:
            messagebox.showwarning("Uyarı", "Önce dosya yükleyin.")
            return
        try:
            flat = petek_katman_normalizasyon(self.raw_array, self.norm_type.get())
            n, m = self.raw_array.shape
            mat = flat[:n*m].reshape(n, m)
            self.normalized_array = mat
            df = self.df_full.copy()
            for idx, col in enumerate(df.select_dtypes(include=[np.number]).columns):
                df[f"{col}_PN"] = mat[:, idx]
            self.display_dataframe(df)
            self.set_status("Normalizasyon uygulandı.", "green")
        except Exception as e:
            messagebox.showerror("Hata", f"Normalizasyon başarısız:\n{e}")

    def save_data(self):
        if self.normalized_array is None:
            messagebox.showwarning("Uyarı", "Önce normalizasyon yapın.")
            return
        fp = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                          filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if not fp: return
        try:
            df = self.df_full.copy()
            for idx, col in enumerate(df.select_dtypes(include=[np.number]).columns):
                df[f"{col}_PN"] = self.normalized_array[:, idx]
            if fp.lower().endswith(".csv"):
                df.to_csv(fp, index=False)
            else:
                df.to_excel(fp, index=False)
            self.set_status(f"Kaydedildi: {fp}", "blue")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme başarısız:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    # Tema seçimi (eğer yüklüyse 'clam', 'alt', 'default', 'classic')
    style = ttk.Style(root)
    style.theme_use('clam')
    PetekNormApp(root)
    root.mainloop()
