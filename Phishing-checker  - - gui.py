import requests
from stem import Signal
from stem.control import Controller
import tkinter as tk
from tkinter import messagebox

# Function to initialize TOR proxy
def init_tor_proxy():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password")  # Set the control password in your torrc file
        controller.signal(Signal.NEWNYM)

# Function to check the URL via proxy
def check_url_via_proxy(url):
    proxy = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050",
    }
    try:
        response = requests.get(url, proxies=proxy, timeout=10)
        if response.status_code == 200:
            return "This link is safe", "green"
        else:
            return "THIS LINK IS NOT SAFE", "red"
    except Exception as e:
        return "Error checking the link", "red"

# Function to check the URL in the GUI
def check_url_gui():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return
    result, color = check_url_via_proxy(url)
    result_label.config(text=result, fg=color)

# Function to launch GUI
def launch_gui():
    root = tk.Tk()
    root.title("Phishing URL Checker with Proxy")

    tk.Label(root, text="Enter URL:").pack(pady=10)
    global url_entry
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    tk.Button(root, text="Check URL", command=check_url_gui).pack(pady=10)

    global result_label
    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack(pady=20)

    root.mainloop()

# Main script logic
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Phishing URL Checker")
    parser.add_argument("--gui", action="store_true", help="Launch GUI mode")
    args = parser.parse_args()

    if args.gui:
        init_tor_proxy()  # Initialize the TOR proxy
        launch_gui()
    else:
        print("Running in CLI mode...")
