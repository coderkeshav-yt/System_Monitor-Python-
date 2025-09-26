# 🖥️ Advanced System Monitor

A modern **desktop system monitoring tool** built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), [psutil](https://github.com/giampaolo/psutil), and [Matplotlib](https://matplotlib.org/).
It provides real-time insights into **CPU, RAM, processes, disk, network, and system information** in a clean tabbed interface.

---

## ✨ Features

* 📊 **Dashboard**:

  * Real-time CPU & RAM usage graph.
  * Progress bars with usage stats.

* ⚡ **Performance**:

  * Per-core CPU usage.
  * Network download/upload speed.
  * Disk read/write speed.

* 🔍 **Processes**:

  * Top 5 CPU-intensive processes.
  * Displays PID, name, and CPU %.

* 🖥️ **System Info**:

  * OS, node name, machine type, processor details.
  * Boot time, physical & logical core count.

* 🎨 **Modern UI**:

  * Dark/light/system theme support.
  * Smooth integration of Matplotlib charts inside Tkinter.

## 📸 Screenshots (optional)

<p align="center"> <img src="https://res.cloudinary.com/dlvxjnycr/image/upload/v1758877392/Dashboard_qsgfj2.png" alt="Weather App Screenshot - Fahrenheit" width="45%"/> &nbsp;&nbsp; <img src="https://res.cloudinary.com/dlvxjnycr/image/upload/v1758877405/performance_l6gilx.png" alt="Weather App Screenshot - Weather Info" width="45%"/> </p>


## 📦 Requirements

Make sure you have Python 3.8+ installed. Then install dependencies:

```bash
pip install customtkinter psutil matplotlib
```

Optional (for NVIDIA GPU monitoring support):

```bash
pip install nvidia-ml-py3
```

---

## 🚀 Usage

Run the app with:

```bash
python system_monitor.py
```

---

## 📂 Project Structure


.
├── system_monitor.py   # Main application
├── README.md           # Documentation
```

## 📜 License

This project is open-source under the **MIT License**.


