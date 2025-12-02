# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import re
import threading
from datetime import datetime
from PIL import Image, ImageTk
import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

std_diameters = [i/8 for i in range(4, 32*8 + 1)]
def nearest_std_diameter(val):
    diffs = [(abs(val - d), d) for d in std_diameters]
    return min(diffs)[1]

std_lengths = [i/4 for i in range(4, 45*4 + 1)]
def nearest_std_length(val):
    diffs = [(abs(val - d), d) for d in std_lengths]
    return min(diffs)[1]

def parse_number(txt):
    txt = txt.replace('"', '')
    txt = re.sub(r'\s*-\s*', '-', txt)
    txt = txt.replace(' ', '')
    if '-' in txt and '/' in txt:
        base, frac = txt.split('-', 1)
        if '/' in frac:
            parts = frac.split('/')
            if len(parts) != 2:
                return None
            num, den = parts
            if den == '0' or den == '' or num == '':
                return None
            return float(base) + (float(num)/float(den))
        return None
    if '/' in txt:
        parts = txt.split('/')
        if len(parts) != 2:
            return None
        num, den = parts
        if den == '0' or den == '' or num == '':
            return None
        return float(num) / float(den)
    try:
        return float(txt)
    except:
        return None

pat_fraction   = r'([0-9]+[ ]?[0-9]/[0-9])'
pat_mixed      = r'([0-9]+\s*-\s*[0-9]/[0-9])'
pat_frac_pure  = r'([0-9]/[0-9])'
pat_decimal    = r'([0-9]+(?:\.[0-9]+)?)'
pat_diam_keywords = r'(Ø|DIAM|DIA|PULG|IN|"|ESPARRAGO|ESPÁRRAGO|STUD)'

def is_mm_value(text, pos):
    window = text[max(0, pos-12):pos+12]
    return "MM" in window

def extract_diameter_with_pos(text):
    if pd.isna(text):
        return None, None
    t = text.upper()
    candidates = []
    for m in re.finditer(fr'{pat_mixed}|{pat_fraction}|{pat_frac_pure}|{pat_decimal}', t):
        raw = m.group(0)
        val = parse_number(raw)
        pos = m.start()
        if val is None:
            continue
        candidates.append((val, pos, raw))
    for val, pos, raw in candidates:
        if not (0.5 <= val <= 4.0):
            continue
        window = t[max(0, pos-15):pos+15]
        if re.search(pat_diam_keywords, window):
            snapped = nearest_std_diameter(val)
            return snapped, pos
    for val, pos, raw in candidates:
        if 0.5 <= val <= 4.0:
            snapped = nearest_std_diameter(val)
            return snapped, pos
    return None, None

def extract_length(text, diameter_pos):
    if pd.isna(text) or diameter_pos is None:
        return None
    t = text.upper()
    candidates = []
    for m in re.finditer(fr'{pat_mixed}|{pat_fraction}|{pat_frac_pure}|{pat_decimal}', t):
        raw = m.group(0)
        val = parse_number(raw)
        pos = m.start()
        if val is None:
            continue
        candidates.append((val, pos, raw))
    after = [(val, pos, raw) for (val, pos, raw) in candidates if pos > diameter_pos]
    if not after:
        return None
    for val, pos, raw in after:
        if is_mm_value(t, pos):
            continue
        if 1.0 <= val <= 45.0:
            return nearest_std_length(val)
    for val, pos, raw in after:
        if is_mm_value(t, pos):
            continue
        if 1.0 <= val <= 45.0:
            return nearest_std_length(val)
    return None

def apply_dimension_extraction(df):
    df['diameter'], df['diameter_pos'] = zip(*df['descripciones'].apply(extract_diameter_with_pos))
    df['length'] = df.apply(lambda row: extract_length(row['descripciones'], row['diameter_pos']), axis=1)
    return df

def extract_dims_on_column(df, col_name):
    tmp = df.copy()
    tmp['descripciones'] = tmp[col_name].astype(str)
    tmp = apply_dimension_extraction(tmp)
    return tmp

def allocate_and_summarize(
    vis_df,
    inv_df,
    col_vis_desc,
    col_inv_desc,
    col_sap,
    col_inv_qty,
    col_vis_udc,
    col_vis_fecha,
    col_vis_req_qty
):
    vis_dims = extract_dims_on_column(vis_df, col_vis_desc)
    inv_dims = extract_dims_on_column(inv_df, col_inv_desc)

    inv_dims['descripciones'] = inv_dims['descripciones'].astype(str)
    inv_dims['descripciones_upper'] = inv_dims['descripciones'].str.upper()
    inv_dims = inv_dims[inv_dims['descripciones_upper'].str.startswith("ESP")]

    inv_dims['sap'] = inv_df[col_sap].astype(str)
    inv_dims['qty_total'] = pd.to_numeric(inv_df[col_inv_qty], errors='coerce').fillna(0)
    inv_dims['remaining'] = inv_dims['qty_total'].copy()

    vis_dims['udc'] = vis_df[col_vis_udc].astype(str)
    vis_dims['fecha'] = vis_df[col_vis_fecha].astype(str)
    vis_dims['req_qty'] = pd.to_numeric(vis_df[col_vis_req_qty], errors='coerce').fillna(0)

    registros = []
    consecutivo = 1

    for idx, row in vis_dims.iterrows():
        d = row['diameter']
        l = row['length']
        req = row['req_qty']
        udc = row['udc']
        fecha = row['fecha']
        desc_sol = vis_df.loc[idx, col_vis_desc]

        asignaciones = []
        desc_entregadas = []
        asignado_total = 0.0

        if (not pd.isna(d)) and (not pd.isna(l)) and req > 0:
            needed = req
            candidates = inv_dims[
                (inv_dims['diameter'] == d) &
                (inv_dims['length'] == l) &
                (inv_dims['remaining'] > 0)
            ]
            for inv_idx, inv_row in candidates.iterrows():
                if needed <= 0:
                    break
                disponible = inv_row['remaining']
                tomar = min(disponible, needed)
                if tomar <= 0:
                    continue
                asignaciones.append((inv_row['sap'], tomar))
                desc_entregadas.append(f"{inv_row[col_inv_desc]} ({tomar})")
                inv_dims.at[inv_idx, 'remaining'] = disponible - tomar
                needed -= tomar
                asignado_total += tomar

        codigos_str = "; ".join(f"{sap} ({cant})" for sap, cant in asignaciones)
        entregadas_str = "; ".join(desc_entregadas)
        porcentaje = (asignado_total / req * 100.0) if req > 0 else 0.0

        registros.append({
            "No.": consecutivo,
            "UDC": udc,
            "Fecha programa": fecha,
            "Descripción solicitada": desc_sol,
            "Descripciones entregadas": entregadas_str,
            "Diámetro": d,
            "Longitud": l,
            "Cantidad requerida": float(req),
            "Cantidad surtida": float(asignado_total),
            "% cubierto": round(porcentaje, 2),
            "Códigos SAP asignados": codigos_str
        })
        consecutivo += 1

    detalle_df = pd.DataFrame(registros)

    if detalle_df.empty:
        resumen_df = pd.DataFrame(columns=["UDC", "Cantidad requerida", "Cantidad surtida", "Porcentaje solvencia %"])
    else:
        grp = detalle_df.groupby("UDC")
        resumen_df = grp.agg({
            "Cantidad requerida": "sum",
            "Cantidad surtida": "sum"
        }).reset_index()
        resumen_df["Porcentaje solvencia %"] = resumen_df.apply(
            lambda r: round((r["Cantidad surtida"] / r["Cantidad requerida"] * 100.0), 2)
            if r["Cantidad requerida"] > 0 else 0.0,
            axis=1
        )

    return detalle_df, resumen_df

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ARGOS – Asignación Inteligente de Espárragos")
        self.geometry("1350x780")
        bg = "#2a3238"
        self.configure(bg=bg)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCombobox", fieldbackground="#0d1216", background="#0d1216", foreground="#ffffff")
        style.configure("Treeview", background="#111820", fieldbackground="#111820", foreground="#ffffff", rowheight=22)
        style.map("Treeview", background=[("selected", "#305070")], foreground=[("selected", "#ffffff")])
        style.configure("Treeview.Heading", background="#1f2730", foreground="#f0f0f0")

        self.inv_df = None
        self.vis_df = None

        self.col_vis_desc = tk.StringVar()
        self.col_inv_desc = tk.StringVar()
        self.col_sap = tk.StringVar()
        self.col_inv_qty = tk.StringVar()
        self.col_vis_udc = tk.StringVar()
        self.col_vis_fecha = tk.StringVar()
        self.col_vis_req_qty = tk.StringVar()

        self.detalle_df = None
        self.resumen_df = None

        self.search_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        bg = "#2a3238"
        fg = "#e8e8e8"
        accent = "#4f6b7a"

        self.top_frame = tk.Frame(self, bg=bg)
        self.top_frame.pack(padx=10, pady=10, fill="x")

        self.logo_frame = tk.Frame(self.top_frame, bg=bg)
        try:
            logo_file = resource_path("logo_argos.png")
            img = Image.open(logo_file)
            img = img.resize((230, 230), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.logo_frame, image=self.logo_img, bg=bg).pack()
        except:
            tk.Label(self.logo_frame, text="Logo no encontrado", bg=bg, fg=fg).pack()

        self.invf = tk.LabelFrame(self.top_frame, text="Inventario (almacén)", bg=bg, fg=fg)
        self.invf.pack(side="left", padx=10, fill="y")
        tk.Button(self.invf, text="Cargar Inventario (.xlsx)", bg=accent, fg=fg, relief="flat", command=self.load_inventory).pack(pady=5, anchor="w")
        tk.Label(self.invf, text="Descripción Inventario", bg=bg, fg=fg).pack(anchor="w")
        self.cmb_inv_desc = ttk.Combobox(self.invf, textvariable=self.col_inv_desc, state="readonly", width=50)
        self.cmb_inv_desc.pack(pady=3)
        tk.Label(self.invf, text="Código SAP", bg=bg, fg=fg).pack(anchor="w")
        self.cmb_sap = ttk.Combobox(self.invf, textvariable=self.col_sap, state="readonly", width=50)
        self.cmb_sap.pack(pady=3)
        tk.Label(self.invf, text="Cantidad disponible", bg=bg, fg=fg).pack(anchor="w")
        self.cmb_inv_qty = ttk.Combobox(self.invf, textvariable=self.col_inv_qty, state="readonly", width=50)
        self.cmb_inv_qty.pack(pady=3)

        self.visf = tk.LabelFrame(self.top_frame, text="Visiflex (ingeniería)", bg=bg, fg=fg)
        self.visf.pack(side="left", padx=10, fill="y")
        tk.Button(self.visf, text="Cargar Visiflex (.xlsx)", bg=accent, fg=fg, relief="flat", command=self.load_visiflex).pack(pady=5, anchor="w")
        tk.Label(self.visf, text="UDC", bg=bg, fg=fg).pack(anchor="w")
        self.cmb_vis_udc = ttk.Combobox(self.visf, textvariable=self.col_vis_udc, state="readonly", width=50)
        self.cmb_vis_udc.pack(pady=3)
        tk.Label(self.visf, text="Fecha programa", bg=bg, fg=fg).pack(anchor="w")
        self.cmb_vis_fecha = ttk.Combobox(self.visf, textvariable=self.col_vis_fecha, state="readonly", width=50)
        self.cmb_vis_fecha.pack(pady=3)
        tk.Label(self.visf, text="Descripción solicitada", bg=bg, fg=fg).pack(anchor="w")
        self.cmb_vis_desc = ttk.Combobox(self.visf, textvariable=self.col_vis_desc, state="readonly", width=50)
        self.cmb_vis_desc.pack(pady=3)
        tk.Label(self.visf, text="Cantidad requerida", bg=bg, fg=fg).pack(anchor="w")
        self.cmb_vis_req_qty = ttk.Combobox(self.visf, textvariable=self.col_vis_req_qty, state="readonly", width=50)
        self.cmb_vis_req_qty.pack(pady=3)
        tk.Button(self.visf, text="Ejecutar asignación", bg=accent, fg=fg, relief="flat", command=self.run_thread).pack(pady=20, anchor="w")

        self.after(200, self._reposition_logo)
        self.bind("<Configure>", self._reposition_logo)

        search_frame = tk.Frame(self, bg=bg)
        search_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(search_frame, text="Búsqueda rápida (Inventario):", bg=bg, fg=fg).pack(side="left")

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=50, bg="#0d1216", fg="#ffffff", insertbackground="#ffffff")
        search_entry.pack(side="left", padx=10)

        tk.Button(search_frame, text="Buscar", bg=accent, fg=fg, relief="flat", command=self.quick_search).pack(side="left", padx=5)

        table_frame = tk.Frame(self, bg=bg)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=[], show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)

        self.status = tk.Label(self, text="Listo", bg=bg, fg=fg)
        self.status.pack(anchor="e", padx=10, pady=5)

    def _reposition_logo(self, event=None):
        try:
            top = self.top_frame
            visf = self.visf
            logo = self.logo_frame

            top.update_idletasks()
            visf.update_idletasks()
            logo.update_idletasks()

            top_w = top.winfo_width()
            visf_x = visf.winfo_x()
            visf_w = visf.winfo_width()
            visf_y = visf.winfo_y()
            visf_h = visf.winfo_height()

            right_edge = top_w
            visf_right = visf_x + visf_w
            space = max(right_edge - visf_right, 0)
            center_x = visf_right + (space / 2)
            center_y = visf_y + visf_h / 2

            logo.place(in_=top, x=center_x, y=center_y, anchor="center")

        except:
            pass

    def load_inventory(self):
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if not path:
            return
        self.inv_df = pd.read_excel(path)
        cols = list(self.inv_df.columns)
        self.cmb_inv_desc["values"] = cols
        self.cmb_sap["values"] = cols
        self.cmb_inv_qty["values"] = cols
        self.status["text"] = "Inventario cargado"

    def load_visiflex(self):
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if not path:
            return
        self.vis_df = pd.read_excel(path)
        cols = list(self.vis_df.columns)
        self.cmb_vis_udc["values"] = cols
        self.cmb_vis_fecha["values"] = cols
        self.cmb_vis_desc["values"] = cols
        self.cmb_vis_req_qty["values"] = cols
        self.status["text"] = "Visiflex cargado"

    def run_thread(self):
        t = threading.Thread(target=self.run_safe, daemon=True)
        t.start()

    def run_safe(self):
        try:
            self.status["text"] = "Procesando..."
            self.run_process()
            self.status["text"] = "Listo"
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status["text"] = "Error"

    def run_process(self):
        if self.inv_df is None or self.vis_df is None:
            raise ValueError("Carga Inventario y Visiflex primero.")

        col_inv_desc = self.col_inv_desc.get()
        col_sap = self.col_sap.get()
        col_inv_qty = self.col_inv_qty.get()
        col_vis_udc = self.col_vis_udc.get()
        col_vis_fecha = self.col_vis_fecha.get()
        col_vis_desc = self.col_vis_desc.get()
        col_vis_req_qty = self.col_vis_req_qty.get()

        detalle, resumen = allocate_and_summarize(
            self.vis_df,
            self.inv_df,
            col_vis_desc=col_vis_desc,
            col_inv_desc=col_inv_desc,
            col_sap=col_sap,
            col_inv_qty=col_inv_qty,
            col_vis_udc=col_vis_udc,
            col_vis_fecha=col_vis_fecha,
            col_vis_req_qty=col_vis_req_qty
        )

        self.detalle_df = detalle
        self.resumen_df = resumen

        self.render_table(detalle)

        default_name = f"Espárragos_ARGOS_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], initialfile=default_name)

        if path:
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                detalle.to_excel(writer, sheet_name="Detalle", index=False)
                resumen.to_excel(writer, sheet_name="Resumen", index=False)

    def render_table(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        for c in df.columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160, anchor="w")
        for _, row in df.iterrows():
            vals = [str(row[c]) for c in df.columns]
            self.tree.insert("", "end", values=vals)

    def quick_search(self):
        if self.inv_df is None:
            messagebox.showerror("Error", "Carga primero el archivo de inventario.")
            return

        term = self.search_var.get().strip()
        if not term:
            messagebox.showwarning("Aviso", "Escribe algo para buscar.")
            return

        # Extraemos D y L exactamente con el mismo motor del sistema
        temp_df = pd.DataFrame({"descripciones": [term]})
        temp_dims = apply_dimension_extraction(temp_df)

        d = temp_dims.loc[0, "diameter"]
        l = temp_dims.loc[0, "length"]

        if pd.isna(d) and pd.isna(l):
            messagebox.showinfo("Sin resultados", "No se detectó diámetro ni longitud en tu búsqueda.")
            return

        # Procesamos el inventario con la misma lógica
        col_inv_desc = self.col_inv_desc.get()
        if not col_inv_desc:
            messagebox.showerror("Error", "Selecciona la columna de descripción del inventario.")
            return

        inv_dims = extract_dims_on_column(self.inv_df, col_inv_desc)

        # FILTRO INTELIGENTE EXACTO (igual que asignación)
        mask = pd.Series([True] * len(inv_dims))

        if not pd.isna(d):
            mask &= (inv_dims["diameter"] == d)

        if not pd.isna(l):
            mask &= (inv_dims["length"] == l)

        results = inv_dims[mask]

        if results.empty:
            messagebox.showinfo(
                "Sin coincidencias",
                f"No se encontró nada con Diámetro={d} y Longitud={l}."
            )
            return

        win = tk.Toplevel(self)
        win.title(f"Resultados dimensionales de '{term}'")
        win.geometry("900x500")
        win.configure(bg="#2a3238")

        tree = ttk.Treeview(win, show="headings")
        tree.pack(fill="both", expand=True)

        results["SAP"] = self.inv_df[self.col_sap.get()].astype(str)
        results["CANTIDAD"] = pd.to_numeric(self.inv_df[self.col_inv_qty.get()], errors="coerce").fillna(0)

        cols = ["SAP", col_inv_desc, "diameter", "length", "CANTIDAD"]
        tree["columns"] = cols

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=150, anchor="w")

        for _, row in results[cols].iterrows():
            vals = [str(row[c]) for c in cols]
            tree.insert("", "end", values=vals)


if __name__ == "__main__":
    app = App()
    app.mainloop()
