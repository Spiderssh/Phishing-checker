# Phishing URL Checker

## Overview
The Phishing URL Checker is a Python-based tool designed to help identify potentially malicious URLs. It operates in two modes:
- **CLI Mode**: Command-line interface with color-coded outputs for safe and unsafe links.
- **GUI Mode**: Graphical user interface built with Tkinter for easy interaction.

This tool can also validate URLs anonymously using a headless browser with proxy support, ensuring your IP address is not exposed.

---

## Features
- Detects phishing indicators in URLs.
- Supports anonymous URL validation via Selenium and a TOR proxy.
- CLI mode with a bright yellow banner and color-coded outputs.
- GUI mode with intuitive input and result display.
- Analyzes URL structure and hosting details.

---

## Requirements
1. **Python** (>= 3.7)
2. **Pip**: Ensure Python dependencies can be installed.
3. **Selenium**: For headless browsing.
   ```bash
   pip install selenium
   ```
4. **Google Chrome** and **ChromeDriver**:
   - Download ChromeDriver matching your Chrome version from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/).
   - Place it in your system's PATH or provide its absolute path in the script.
5. **TOR Proxy**:
   - Install and configure TOR for anonymous browsing.
   - Ensure TOR is running on `127.0.0.1:9050`.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Spiderssh/phishing-checker.git
   cd phishing-checker
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### CLI Mode
Run the script in CLI mode:
```bash
python phishing-checker.py
```
Follow the prompts to enter URLs one by one. Type `done` to finish and view the results.

### GUI Mode
Run the script in GUI mode:
```bash
python phishing-checker.py --gui
```
A window will open where you can enter and analyze URLs.

---

## How It Works
1. **Phishing Indicators**:
   - Scans URLs for common phishing terms like `login`, `secure`, `verify`, etc.
   - Flags suspicious top-level domains (e.g., `.xyz`, `.click`).
2. **Anonymous Validation**:
   - Uses Selenium with a headless Chrome browser.
   - Routes traffic through a TOR proxy for anonymity.
   - Checks for valid page loads and HTTPS certificates.
3. **Color-Coded Results**:
   - **Green**: Indicates the URL is safe.
   - **Red**: Indicates the URL is unsafe or problematic.

---

## Example
### CLI Output
```
==================================================
          Phishing URL Checker (CLI Mode)          
==================================================
Enter URLs to analyze (type 'done' to finish):
URL: http://example.com
http://example.com -> [92mThis link is safe[0m
URL: http://phishy-site.xyz
http://phishy-site.xyz -> [91mTHIS LINK IS NOT SAFE[0m
```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Disclaimer
This tool is for educational purposes only. It is not a substitute for professional security software. Always exercise caution when interacting with unknown links.
