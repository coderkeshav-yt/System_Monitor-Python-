import customtkinter as ctk
import psutil
import platform
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from tkinter import ttk

# Optional: For NVIDIA GPU monitoring
try:
    import pynvml
    NVIDIA_SMI_AVAILABLE = True
except ImportError:
    NVIDIA_SMI_AVAILABLE = False

# --- Main Application Class ---
class AdvancedSystemMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced System Monitor")
        self.geometry("900x650")

        # --- Appearance Settings ---
        ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")

        # --- Data Storage for Graphing ---
        self.cpu_data = deque(maxlen=50)
        self.ram_data = deque(maxlen=50)
        self.time_steps = deque(maxlen=50)
        for i in range(50): # Pre-fill with zeros
             self.cpu_data.append(0)
             self.ram_data.append(0)
             self.time_steps.append(i-49)
        
        # --- State for calculating speeds ---
        self.last_net_io = psutil.net_io_counters()
        self.last_disk_io = psutil.disk_io_counters()

        # --- Main Layout (Tabs) ---
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(expand=True, fill="both", padx=10, pady=10)

        self.dashboard_tab = self.tab_view.add("Dashboard")
        self.performance_tab = self.tab_view.add("Performance")
        self.processes_tab = self.tab_view.add("Processes")
        self.system_info_tab = self.tab_view.add("System Info")

        # --- Create content for each tab ---
        self.create_dashboard_tab()
        self.create_performance_tab()
        self.create_processes_tab()
        self.create_system_info_tab()

        # --- Start the update loop ---
        self.update_data()

    def create_dashboard_tab(self):
        # --- Matplotlib Graph ---
        graph_frame = ctk.CTkFrame(self.dashboard_tab)
        graph_frame.pack(pady=10, padx=10, fill="x")
        
        self.fig, self.ax = plt.subplots(figsize=(8, 3), dpi=100)
        self.ax.set_facecolor("#2B2B2B") # Match dark theme
        self.fig.patch.set_facecolor("#2B2B2B")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Real-Time CPU & RAM Usage", color="white")
        self.ax.set_ylabel("Usage (%)", color="white")
        self.cpu_line, = self.ax.plot(list(self.time_steps), list(self.cpu_data), label="CPU", color="#FF5733")
        self.ram_line, = self.ax.plot(list(self.time_steps), list(self.ram_data), label="RAM", color="#33C4FF")
        self.ax.legend(facecolor="#2B2B2B", labelcolor="white")
        self.ax.grid(True, color="#555555")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # --- Main Progress Bars ---
        stats_frame = ctk.CTkFrame(self.dashboard_tab)
        stats_frame.pack(pady=10, padx=10, fill="x")
        stats_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(stats_frame, text="🖥️ CPU:", font=("Helvetica", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.cpu_progress = ctk.CTkProgressBar(stats_frame)
        self.cpu_progress.grid(row=0, column=1, sticky="ew")
        self.cpu_label = ctk.CTkLabel(stats_frame, text="0%", font=("Helvetica", 14))
        self.cpu_label.grid(row=0, column=2, padx=10)

        ctk.CTkLabel(stats_frame, text="🧠 RAM:", font=("Helvetica", 14)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.ram_progress = ctk.CTkProgressBar(stats_frame)
        self.ram_progress.grid(row=1, column=1, sticky="ew")
        self.ram_label = ctk.CTkLabel(stats_frame, text="0%", font=("Helvetica", 14))
        self.ram_label.grid(row=1, column=2, padx=10)

    def create_performance_tab(self):
        perf_frame = ctk.CTkFrame(self.performance_tab)
        perf_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Per-Core CPU
        core_frame = ctk.CTkFrame(perf_frame)
        core_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(core_frame, text="Per-Core CPU Usage", font=("Helvetica", 16, "bold")).pack()
        
        self.core_bars = []
        num_cores = psutil.cpu_count(logical=True)
        for i in range(num_cores):
            frame = ctk.CTkFrame(core_frame)
            frame.pack(fill="x", padx=10, pady=2)
            label = ctk.CTkLabel(frame, text=f"Core {i+1}:", width=80)
            label.pack(side="left")
            bar = ctk.CTkProgressBar(frame)
            bar.pack(side="left", expand=True, fill="x", padx=5)
            self.core_bars.append(bar)

        # Network and Disk
        io_frame = ctk.CTkFrame(perf_frame)
        io_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(io_frame, text="Network & Disk Activity", font=("Helvetica", 16, "bold")).pack()

        self.net_label = ctk.CTkLabel(io_frame, text="🌐 Network: ↓ 0 B/s | ↑ 0 B/s", font=("Helvetica", 14))
        self.net_label.pack(pady=5)
        self.disk_label = ctk.CTkLabel(io_frame, text="💾 Disk: R 0 B/s | W 0 B/s", font=("Helvetica", 14))
        self.disk_label.pack(pady=5)

    def create_processes_tab(self):
        proc_frame = ctk.CTkFrame(self.processes_tab)
        proc_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(proc_frame, text="Top 5 CPU Intensive Processes", font=("Helvetica", 16, "bold")).pack(pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B", borderwidth=0)
        style.map('Treeview', background=[('selected', '#2A2D2E')])
        style.configure("Treeview.Heading", background="#565B5E", foreground="white", relief="flat")
        
        self.process_tree = ttk.Treeview(proc_frame, columns=("pid", "name", "cpu"), show="headings")
        self.process_tree.heading("pid", text="PID")
        self.process_tree.heading("name", text="Name")
        self.process_tree.heading("cpu", text="CPU %")
        self.process_tree.pack(expand=True, fill="both")

    def create_system_info_tab(self):
        info_frame = ctk.CTkFrame(self.system_info_tab)
        info_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        info_text = f"""
        System: {platform.system()} {platform.release()}
        Node Name: {platform.node()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        Boot Time: {boot_time}
        CPU Cores (Physical): {psutil.cpu_count(logical=False)}
        CPU Cores (Logical): {psutil.cpu_count(logical=True)}
        """
        ctk.CTkLabel(info_frame, text=info_text, font=("Helvetica", 14), justify="left").pack(anchor="w")


    def update_data(self):
        # --- Dashboard Tab Update ---
        cpu_percent = psutil.cpu_percent()
        mem_info = psutil.virtual_memory()

        self.cpu_data.append(cpu_percent)
        self.ram_data.append(mem_info.percent)
        self.time_steps.append(self.time_steps[-1] + 1)
        
        self.cpu_line.set_ydata(list(self.cpu_data))
        self.ram_line.set_ydata(list(self.ram_data))
        self.ax.set_xlim(self.time_steps[0], self.time_steps[-1])
        self.canvas.draw()
        
        self.cpu_progress.set(cpu_percent / 100)
        self.cpu_label.configure(text=f"{cpu_percent:.1f}%")
        self.ram_progress.set(mem_info.percent / 100)
        self.ram_label.configure(text=f"{mem_info.percent}% ({mem_info.used/1024**3:.1f}/{mem_info.total/1024**3:.1f} GB)")

        # --- Performance Tab Update ---
        per_cpu = psutil.cpu_percent(percpu=True)
        for i, bar in enumerate(self.core_bars):
            bar.set(per_cpu[i] / 100)

        current_net_io = psutil.net_io_counters()
        net_sent = current_net_io.bytes_sent - self.last_net_io.bytes_sent
        net_recv = current_net_io.bytes_recv - self.last_net_io.bytes_recv
        self.net_label.configure(text=f"🌐 Network: ↓ {net_recv/1024:.1f} KB/s | ↑ {net_sent/1024:.1f} KB/s")
        self.last_net_io = current_net_io

        current_disk_io = psutil.disk_io_counters()
        disk_read = current_disk_io.read_bytes - self.last_disk_io.read_bytes
        disk_write = current_disk_io.write_bytes - self.last_disk_io.write_bytes
        self.disk_label.configure(text=f"💾 Disk: R {disk_read/1024:.1f} KB/s | W {disk_write/1024:.1f} KB/s")
        self.last_disk_io = current_disk_io
        
        # --- Processes Tab Update ---
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        top_processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:5]
        
        for i in self.process_tree.get_children():
            self.process_tree.delete(i)
        for proc in top_processes:
            self.process_tree.insert("", "end", values=(proc['pid'], proc['name'], f"{proc['cpu_percent']:.2f}"))

        # --- Schedule next update ---
        self.after(1000, self.update_data)

# --- Main execution ---
if __name__ == "__main__":
    app = AdvancedSystemMonitor()
    app.mainloop()