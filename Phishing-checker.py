# phishing-checker.py
# A script to identify potential phishing URLs using CLI or GUI environments.

import re
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tkinter import Tk, Label, Button, Entry, StringVar

def is_phishing_url(url):
    """
    Checks if a URL contains potential phishing indicators.

    Args:
        url (str): The URL to analyze.

    Returns:
        bool: True if the URL is likely phishing, False otherwise.
    """
    phishing_indicators = [
        'login', 'secure', 'account', 'verify', 'webscr', 'update', 'auth', 'signin'
    ]

    suspicious_tlds = [
        '.xyz', '.click', '.top', '.tk', '.ml', '.ga', '.cf', '.gq','[.]com','.beauty','.buzz','.shop','.cf','.cn','.trycloudflare.com','.dad','.zip','.mov','.nexus','.club','.icu','.host','.ru','.ru<','.wang','gq','.ml'
    ]

    # Check for phishing indicators in the URL path or query parameters
    if any(indicator in url.lower() for indicator in phishing_indicators):
        return True

    # Check if the URL uses a suspicious top-level domain (TLD)
    if any(url.lower().endswith(tld) for tld in suspicious_tlds):
        return True

    return False

def check_url_safety(url):
    """
    Validate the legitimacy of the URL by loading it anonymously.

    Args:
        url (str): The URL to check.

    Returns:
        str: Result message indicating whether the link is safe or not.
    """
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--proxy-server=socks5://127.0.0.1:9050')  # Use TOR proxy for anonymity

        service = Service('/path/to/chromedriver')  # Update with the path to your ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        # Verify if the page loaded successfully (no redirection or errors)
        if "error" in driver.title.lower() or "not found" in driver.title.lower():
            return "THIS LINK IS NOT SAFE"

        driver.quit()
        return "This link is safe"

    except Exception as e:
        return f"THIS LINK IS NOT SAFE ({str(e)})"

def analyze_urls(urls):
    """
    Analyze a list of URLs and print whether each one is safe or a potential phishing link.

    Args:
        urls (list): A list of URLs to analyze.
    """
    for url in urls:
        if is_phishing_url(url):
            print(f"\033[91m{url} -> THIS LINK IS NOT SAFE\033[0m")  # Red color
        else:
            safety_check = check_url_safety(url)
            if "safe" in safety_check.lower():
                print(f"\033[92m{url} -> {safety_check}\033[0m")  # Green color
            else:
                print(f"\033[91m{url} -> {safety_check}\033[0m")  # Red color

def cli_mode():
    """
    Command Line Interface mode with a bright yellow banner.
    """
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[93m")  # Bright yellow color
    print("=" * 50)
    print(" Phishing URL Checker (CLI Mode) ".center(50))
    print("=" * 50)
    print("\033[0m")  # Reset color

    urls = []
    print("Enter URLs to analyze (type 'done' to finish):")
    while True:
        url = input("URL: ").strip()
        if url.lower() == 'done':
            break
        urls.append(url)

    analyze_urls(urls)

def gui_mode():
    """
    Graphical User Interface mode using Tkinter.
    """
    def analyze():
        url = url_input.get()
        if url:
            if is_phishing_url(url):
                result_label.config(text="THIS LINK IS NOT SAFE", fg="red")
            else:
                safety_check = check_url_safety(url)
                if "safe" in safety_check.lower():
                    result_label.config(text="This link is safe", fg="green")
                else:
                    result_label.config(text=safety_check, fg="red")

    root = Tk()
    root.title("Phishing URL Checker")

    Label(root, text="Enter a URL to analyze:").pack(pady=5)
    url_input = StringVar()
    Entry(root, textvariable=url_input, width=50).pack(pady=5)
    Button(root, text="Check", command=analyze).pack(pady=10)

    result_label = Label(root, text="", font=("Arial", 12))
    result_label.pack(pady=5)

    Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        gui_mode()
    else:
        cli_mode()
