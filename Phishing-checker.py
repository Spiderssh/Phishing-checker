# phishing-checker.py
# A script to identify potential phishing URLs using CLI or GUI environments.

import re
import os
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tkinter import Tk, Label, Button, Entry, StringVar

TOR_PROXY = "socks5h://127.0.0.1:9050"

def configure_tor_session():
    """
    Configure a TOR session for anonymous HTTP requests.

    Returns:
        requests.Session: A configured session object.
    """
    session = requests.Session()
    session.proxies = {
        "http": TOR_PROXY,
        "https": TOR_PROXY,
    }
    return session

def analyze_url_tor(url):
    """
    Analyze a URL for malicious activity via a TOR connection.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: Analysis results including page behavior and reputation.
    """
    session = configure_tor_session()
    results = {
        "url": url,
        "safe": True,
        "reason": "No malicious activity detected.",
    }

    try:
        # Fetch the page content
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            # Check for suspicious keywords in content
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title.string if soup.title else ""
            if any(keyword in title.lower() for keyword in ["login", "verify", "auth", "secure"]):
                results["safe"] = False
                results["reason"] = "Suspicious keywords found in page title."

            # Additional checks for redirection or malformed content
            if "meta http-equiv='refresh'" in str(soup).lower():
                results["safe"] = False
                results["reason"] = "Page contains redirection behavior."

        else:
            results["safe"] = False
            results["reason"] = f"HTTP error code: {response.status_code}"

    except Exception as e:
        results["safe"] = False
        results["reason"] = f"Error during analysis: {str(e)}"

    return results

def selenium_tor_analysis(url):
    """
    Perform deeper analysis using Selenium over a TOR proxy.

    Args:
        url (str): The URL to analyze.

    Returns:
        str: Result of the analysis.
    """
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--proxy-server=socks5://127.0.0.1:9050")  # Use TOR proxy

        service = Service('/path/to/chromedriver')  # Update with the path to your ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        # Check for suspicious content or redirections
        if "login" in driver.title.lower() or "auth" in driver.title.lower():
            driver.quit()
            return "THIS LINK IS NOT SAFE: Contains suspicious keywords in title."

        driver.quit()
        return "This link is safe."

    except Exception as e:
        return f"Error during Selenium analysis: {str(e)}"

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

    # Check for phishing indicators in the URL path or query parameters
    if any(indicator in url.lower() for indicator in phishing_indicators):
        return True

    return False

def analyze_urls(urls):
    """
    Analyze a list of URLs and print whether each one is safe or a potential phishing link.

    Args:
        urls (list): A list of URLs to analyze.
    """
    for url in urls:
        tor_results = analyze_url_tor(url)
        if not tor_results["safe"]:
            print(f"\033[91m{url} -> {tor_results['reason']}\033[0m")  # Red color
        else:
            selenium_results = selenium_tor_analysis(url)
            if "safe" in selenium_results.lower():
                print(f"\033[92m{url} -> {selenium_results}\033[0m")  # Green color
            else:
                print(f"\033[91m{url} -> {selenium_results}\033[0m")  # Red color

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
            tor_results = analyze_url_tor(url)
            if not tor_results["safe"]:
                result_label.config(text=tor_results['reason'], fg="red")
            else:
                selenium_results = selenium_tor_analysis(url)
                if "safe" in selenium_results.lower():
                    result_label.config(text=selenium_results, fg="green")
                else:
                    result_label.config(text=selenium_results, fg="red")

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
