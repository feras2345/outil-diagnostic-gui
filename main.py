import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
import json
import os
from datetime import datetime

class DiagnosticToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Outil de Diagnostic Système")
        self.root.geometry("1200x700")
        
        # Style moderne
        self.style = ttk_bs.Style(theme='darkly')
        
        # Variables
        self.current_data = None
        self.data_folder = "data"
        
        # Créer l'interface
        self.create_widgets()
        
    def create_widgets(self):
        # En-tête
        header_frame = ttk_bs.Frame(self.root, bootstyle="primary")
        header_frame.pack(fill=X, padx=10, pady=10)
        
        title_label = ttk_bs.Label(
            header_frame, 
            text="🖥️ Outil de Diagnostic Système", 
            font=("Helvetica", 20, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(pady=15)
        
        # Frame principal avec 2 colonnes
        main_frame = ttk_bs.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        # Colonne gauche - Menu
        left_frame = ttk_bs.Frame(main_frame, bootstyle="secondary")
        left_frame.pack(side=LEFT, fill=Y, padx=(0, 5))
        
        menu_label = ttk_bs.Label(
            left_frame, 
            text="📋 Modules", 
            font=("Helvetica", 14, "bold"),
            bootstyle="inverse-secondary"
        )
        menu_label.pack(pady=10, padx=10)
        
        # Boutons de menu
        self.create_menu_button(left_frame, "🖥️ Diagnostic Windows", self.show_windows_diagnostic)
        self.create_menu_button(left_frame, "🗄️ Vérification MySQL", self.show_mysql_check)
        self.create_menu_button(left_frame, "🌐 Scan Réseau", self.show_network_scan)
        self.create_menu_button(left_frame, "⚠️ Audit Obsolescence", self.show_obsolescence_audit)
        self.create_menu_button(left_frame, "📊 Base EOL", self.show_eol_database)
        
        ttk_bs.Separator(left_frame, orient=HORIZONTAL).pack(fill=X, pady=10, padx=10)
        
        self.create_menu_button(left_frame, "📂 Charger fichier JSON", self.load_json_file, bootstyle="info")
        self.create_menu_button(left_frame, "🔄 Rafraîchir", self.refresh_data, bootstyle="success")
        
        # Colonne droite - Contenu
        right_frame = ttk_bs.Frame(main_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        # Zone de contenu avec scrollbar
        self.content_frame = ttk_bs.Frame(right_frame)
        self.content_frame.pack(fill=BOTH, expand=YES)
        
        # Canvas pour scrolling
        canvas = tk.Canvas(self.content_frame, bg='#2b3e50', highlightthickness=0)
        scrollbar = ttk_bs.Scrollbar(self.content_frame, orient=VERTICAL, command=canvas.yview, bootstyle="primary-round")
        
        self.scrollable_frame = ttk_bs.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Message de bienvenue
        self.show_welcome()
        
    def create_menu_button(self, parent, text, command, bootstyle="secondary"):
        btn = ttk_bs.Button(
            parent, 
            text=text, 
            command=command,
            bootstyle=bootstyle,
            width=25
        )
        btn.pack(pady=5, padx=10, fill=X)
        
    def clear_content(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
    def show_welcome(self):
        self.clear_content()
        welcome_label = ttk_bs.Label(
            self.scrollable_frame,
            text="👋 Bienvenue dans l'Outil de Diagnostic Système\n\n"
                 "Sélectionnez un module dans le menu de gauche pour commencer.",
            font=("Helvetica", 14),
            bootstyle="inverse-dark",
            justify=CENTER
        )
        welcome_label.pack(pady=100, padx=20)
        
    def load_json_file(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.display_json_data(data, os.path.basename(filename))
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger le fichier:\n{str(e)}")
                
    def display_json_data(self, data, title="Données JSON"):
        self.clear_content()
        
        title_label = ttk_bs.Label(
            self.scrollable_frame,
            text=f"📄 {title}",
            font=("Helvetica", 16, "bold"),
            bootstyle="info"
        )
        title_label.pack(pady=10, padx=10, anchor=W)
        
        # Affichage récursif des données
        self.display_dict(data, self.scrollable_frame)
        
    def display_dict(self, data, parent, level=0):
        if isinstance(data, dict):
            for key, value in data.items():
                frame = ttk_bs.Frame(parent)
                frame.pack(fill=X, padx=(20*level, 10), pady=2, anchor=W)
                
                if isinstance(value, (dict, list)):
                    label = ttk_bs.Label(
                        frame,
                        text=f"▼ {key}:",
                        font=("Helvetica", 11, "bold"),
                        bootstyle="warning"
                    )
                    label.pack(anchor=W)
                    self.display_dict(value, parent, level+1)
                else:
                    label = ttk_bs.Label(
                        frame,
                        text=f"{key}: {value}",
                        font=("Helvetica", 10),
                        bootstyle="light"
                    )
                    label.pack(anchor=W)
                    
        elif isinstance(data, list):
            for i, item in enumerate(data):
                frame = ttk_bs.Frame(parent)
                frame.pack(fill=X, padx=(20*level, 10), pady=2, anchor=W)
                
                label = ttk_bs.Label(
                    frame,
                    text=f"[{i}]",
                    font=("Helvetica", 10, "bold"),
                    bootstyle="info"
                )
                label.pack(anchor=W)
                self.display_dict(item, parent, level+1)
                
    def load_json_from_data_folder(self, filename):
        filepath = os.path.join(self.data_folder, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger {filename}:\n{str(e)}")
                return None
        else:
            messagebox.showwarning("Attention", f"Le fichier {filename} n'existe pas dans le dossier data/")
            return None
            
    def show_windows_diagnostic(self):
        data = self.load_json_from_data_folder("windows_diagnostic_20251106_213357.json")
        if data:
            self.display_windows_diagnostic(data)
            
    def display_windows_diagnostic(self, data):
        self.clear_content()
        
        title = ttk_bs.Label(
            self.scrollable_frame,
            text="🖥️ Diagnostic Windows",
            font=("Helvetica", 18, "bold"),
            bootstyle="info"
        )
        title.pack(pady=15, padx=10)
        
        # Informations système
        info_frame = ttk_bs.Labelframe(
            self.scrollable_frame,
            text="Informations Système",
            bootstyle="primary"
        )
        info_frame.pack(fill=X, padx=20, pady=10)
        
        info_data = [
            ("Hostname", data.get("hostname", "N/A")),
            ("OS", f"{data.get('os', 'N/A')} {data.get('os_release', '')}"),
            ("Version", data.get("os_version", "N/A")),
            ("Architecture", data.get("architecture", "N/A")),
            ("Uptime", f"{data.get('uptime_days', 0)} jours, {data.get('uptime_hours', 0)} heures"),
        ]
        
        for label_text, value in info_data:
            row = ttk_bs.Frame(info_frame)
            row.pack(fill=X, padx=10, pady=5)
            ttk_bs.Label(row, text=f"{label_text}:", font=("Helvetica", 10, "bold")).pack(side=LEFT)
            ttk_bs.Label(row, text=value, font=("Helvetica", 10)).pack(side=RIGHT)
            
        # Performances
        perf_frame = ttk_bs.Labelframe(
            self.scrollable_frame,
            text="Performances",
            bootstyle="success"
        )
        perf_frame.pack(fill=X, padx=20, pady=10)
        
        # CPU
        cpu_frame = ttk_bs.Frame(perf_frame)
        cpu_frame.pack(fill=X, padx=10, pady=5)
        ttk_bs.Label(cpu_frame, text=f"CPU: {data.get('cpu_percent', 0)}%", font=("Helvetica", 10)).pack(side=LEFT)
        ttk_bs.Progressbar(
            cpu_frame, 
            value=data.get('cpu_percent', 0), 
            bootstyle="success"
        ).pack(side=RIGHT, fill=X, expand=YES, padx=10)
        
        # Mémoire
        mem_frame = ttk_bs.Frame(perf_frame)
        mem_frame.pack(fill=X, padx=10, pady=5)
        mem_percent = data.get('memory_percent', 0)
        ttk_bs.Label(mem_frame, text=f"Mémoire: {mem_percent}%", font=("Helvetica", 10)).pack(side=LEFT)
        ttk_bs.Progressbar(
            mem_frame, 
            value=mem_percent, 
            bootstyle="warning" if mem_percent > 70 else "info"
        ).pack(side=RIGHT, fill=X, expand=YES, padx=10)
        
        # Disques
        if "disks" in data:
            disk_frame = ttk_bs.Labelframe(
                self.scrollable_frame,
                text="Disques",
                bootstyle="warning"
            )
            disk_frame.pack(fill=X, padx=20, pady=10)
            
            for disk in data["disks"]:
                disk_info = ttk_bs.Frame(disk_frame)
                disk_info.pack(fill=X, padx=10, pady=5)
                
                ttk_bs.Label(
                    disk_info, 
                    text=f"{disk.get('device', 'N/A')} - {disk.get('percent', 0)}% utilisé",
                    font=("Helvetica", 10)
                ).pack(side=LEFT)
                
                ttk_bs.Progressbar(
                    disk_info, 
                    value=disk.get('percent', 0),
                    bootstyle="danger" if disk.get('percent', 0) > 80 else "success"
                ).pack(side=RIGHT, fill=X, expand=YES, padx=10)
                
    def show_mysql_check(self):
        data = self.load_json_from_data_folder("mysql_check_20251106_212747.json")
        if data:
            self.display_mysql_check(data)
            
    def display_mysql_check(self, data):
        self.clear_content()
        
        title = ttk_bs.Label(
            self.scrollable_frame,
            text="🗄️ Vérification MySQL",
            font=("Helvetica", 18, "bold"),
            bootstyle="info"
        )
        title.pack(pady=15, padx=10)
        
        status = data.get("status", "UNKNOWN")
        status_color = "danger" if status == "CRITICAL" else "success"
        
        status_frame = ttk_bs.Frame(self.scrollable_frame, bootstyle=status_color)
        status_frame.pack(fill=X, padx=20, pady=10)
        
        ttk_bs.Label(
            status_frame,
            text=f"Status: {status}",
            font=("Helvetica", 14, "bold"),
            bootstyle=f"inverse-{status_color}"
        ).pack(pady=10)
        
        # Détails
        details_frame = ttk_bs.Labelframe(
            self.scrollable_frame,
            text="Détails",
            bootstyle="secondary"
        )
        details_frame.pack(fill=X, padx=20, pady=10)
        
        details = [
            ("Host", data.get("host", "N/A")),
            ("Ping", "✓" if data.get("ping") else "✗"),
            ("Port 3306", "✓" if data.get("port_3306") else "✗"),
            ("Connexion", "✓" if data.get("connection") else "✗"),
        ]
        
        for label_text, value in details:
            row = ttk_bs.Frame(details_frame)
            row.pack(fill=X, padx=10, pady=5)
            ttk_bs.Label(row, text=f"{label_text}:", font=("Helvetica", 10, "bold")).pack(side=LEFT)
            ttk_bs.Label(row, text=value, font=("Helvetica", 10)).pack(side=RIGHT)
            
        if "error" in data:
            error_frame = ttk_bs.Labelframe(
                self.scrollable_frame,
                text="Erreur",
                bootstyle="danger"
            )
            error_frame.pack(fill=X, padx=20, pady=10)
            
            ttk_bs.Label(
                error_frame,
                text=data["error"],
                font=("Helvetica", 10),
                wraplength=700
            ).pack(padx=10, pady=10)
            
    def show_network_scan(self):
        # Chercher le fichier le plus récent
        data = self.load_json_from_data_folder("network_scan_20251107_090850.json")
        if data:
            self.display_json_data(data, "Scan Réseau")
            
    def show_obsolescence_audit(self):
        data = self.load_json_from_data_folder("audit_obsolescence_20251107_143612.json")
        if data:
            self.display_obsolescence_audit(data)
            
    def display_obsolescence_audit(self, data):
        self.clear_content()
        
        title = ttk_bs.Label(
            self.scrollable_frame,
            text="⚠️ Audit d'Obsolescence",
            font=("Helvetica", 18, "bold"),
            bootstyle="warning"
        )
        title.pack(pady=15, padx=10)
        
        # Résumé
        summary = data.get("summary", {})
        summary_frame = ttk_bs.Labelframe(
            self.scrollable_frame,
            text="Résumé",
            bootstyle="info"
        )
        summary_frame.pack(fill=X, padx=20, pady=10)
        
        summary_data = [
            ("Total", summary.get("total", 0), "info"),
            ("Critique", summary.get("critical", 0), "danger"),
            ("Avertissement", summary.get("warning", 0), "warning"),
            ("OK", summary.get("ok", 0), "success"),
            ("Inconnu", summary.get("unknown", 0), "secondary"),
        ]
        
        for label_text, value, color in summary_data:
            row = ttk_bs.Frame(summary_frame)
            row.pack(fill=X, padx=10, pady=5)
            ttk_bs.Label(row, text=f"{label_text}:", font=("Helvetica", 10, "bold")).pack(side=LEFT)
            ttk_bs.Label(
                row, 
                text=str(value), 
                font=("Helvetica", 10, "bold"),
                bootstyle=color
            ).pack(side=RIGHT)
            
        # Hosts critiques
        if data.get("critical_hosts"):
            critical_frame = ttk_bs.Labelframe(
                self.scrollable_frame,
                text="⚠️ Hosts Critiques (EOL Expiré)",
                bootstyle="danger"
            )
            critical_frame.pack(fill=X, padx=20, pady=10)
            
            for host in data["critical_hosts"]:
                host_frame = ttk_bs.Frame(critical_frame, bootstyle="dark")
                host_frame.pack(fill=X, padx=10, pady=5)
                
                ttk_bs.Label(
                    host_frame,
                    text=f"🖥️ {host['hostname']} ({host['ip']})",
                    font=("Helvetica", 11, "bold"),
                    bootstyle="danger"
                ).pack(anchor=W, padx=5, pady=2)
                
                ttk_bs.Label(
                    host_frame,
                    text=f"   OS: {host['os_version']} | EOL: {host['eol_date']}",
                    font=("Helvetica", 9)
                ).pack(anchor=W, padx=5, pady=2)
                
        # Hosts OK
        if data.get("ok_hosts"):
            ok_frame = ttk_bs.Labelframe(
                self.scrollable_frame,
                text="✓ Hosts OK",
                bootstyle="success"
            )
            ok_frame.pack(fill=X, padx=20, pady=10)
            
            for host in data["ok_hosts"]:
                host_frame = ttk_bs.Frame(ok_frame)
                host_frame.pack(fill=X, padx=10, pady=5)
                
                ttk_bs.Label(
                    host_frame,
                    text=f"✓ {host['hostname']} ({host['ip']}) - {host['os_version']}",
                    font=("Helvetica", 10)
                ).pack(anchor=W, padx=5)
                
    def show_eol_database(self):
        data = self.load_json_from_data_folder("eol_database_20251106_212818.json")
        if data:
            self.display_json_data(data, "Base de données EOL")
            
    def refresh_data(self):
        messagebox.showinfo("Rafraîchir", "Données rafraîchies avec succès!")
        self.show_welcome()

def main():
    root = ttk_bs.Window(themename="darkly")
    app = DiagnosticToolGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
