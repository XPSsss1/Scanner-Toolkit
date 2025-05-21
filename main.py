import os
import platform
import webbrowser
import time
import subprocess
import shutil # New import for checking tool existence

# Clear screen (Remains at the top for initial clear)
os.system('cls' if os.name == 'nt' else 'clear')

# Colors - Adjusted for a Red GUI theme
RESET = '\033[0m'
MAGENTA = '\033[95m' # Used for main banner
CYAN = '\033[96m'   # Used for info text
RED = '\033[91m'    # Primary color for boxes, warnings, and accents
YELLOW = '\033[93m' # Used for input prompts
BLUE = '\033[94m'   # Used for messages about opening/executing
GREEN = '\033[92m'  # Used for sub-menu titles and success messages
LIGHT_GRAY = '\033[37m' # For status messages

# --- Banners ---

# Main Banner for the Scanning Multi-Tool
SCANNER_MAIN_BANNER = f"""{RED}
███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     
██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝       ██║   ██║   ██║██║   ██║██║     
╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗       ██║   ██║   ██║██║   ██║██║     
███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
{RESET}"""

# Generic Sub-Menu Banner (can be customized later if needed for each category)
GENERIC_SUB_MENU_BANNER = f"""{RED}
███████╗██╗   ██╗██████╗  ██████╗ ██╗    ██╗███████╗
██╔════╝██║   ██║██╔══██╗██╔═══██╗██║    ██║██╔════╝
█████╗  ██║   ██║██████╔╝██║   ██║██║ █╗ ██║█████╗  
██╔══╝  ██║   ██║██╔══██╗██║   ██║██║███╗██║██╔══╝  
██║     ╚██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══════╝ ╚══════╝
{RESET}"""

# Function to clear screen and display a specific banner
def refresh_and_banner(banner_to_display=SCANNER_MAIN_BANNER):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner_to_display)

# Function to check if a command-line tool is installed and in PATH
def check_tool_installed(tool_name):
    return shutil.which(tool_name) is not None

# Info box
print(f"{CYAN}Made with <3 by ANS! - version 1.1{RESET}") # Updated version
print(f"{RED}╔══════════════════════════════════════════════════════╗")
print(f"║{RESET} {CYAN}[!] This tool requires external scanners to be installed.{RED} ║")
print(f"║{RESET} {CYAN}[!] Use option [11] to check installed tools.           {RED} ║") # Added tip
print(f"╚══════════════════════════════════════════════════════╝{RESET}")

# Menu boxes for the main categories
left_menu = [
    "[1] > Network & Port Scanners",
    "[2] > Web Vulnerability Scanners",
    "[3] > Subdomain & Recon Scanners",
    "[4] > CMS & Specific App Scanners",
    "[5] > Authentication & Credential Scanners",
]

right_menu = [
    "[6] > Content Discovery Scanners",
    "[7] > Cloud & Container Scanners",
    "[8] > Code Analysis (SAST) Scanners",
    "[9] > Other / Advanced Scanners",
    "[10]> Coming Soon...",
    "[11]> Check Tool Status", # New option
]

# Draw boxes
def draw_box(left, right):
    # Determine max height for consistent box drawing
    max_len = max(len(left), len(right))

    print(f"{RED}╔{'═'*35}╗    ╔{'═'*35}╗")
    for i in range(max_len):
        l_item = left[i] if i < len(left) else ""
        r_item = right[i] if i < len(right) else ""
        print(f"║ {CYAN}{l_item:<33}{RED}║    ║ {CYAN}{r_item:<33}{RED}║")
    print(f"╚{'═'*35}╝    ╚{'═'*35}╝{RESET}")

draw_box(left_menu, right_menu)

# Function to run external scanner commands
def run_scanner(tool_name, command_template, tip_message, banner_to_use=GENERIC_SUB_MENU_BANNER):
    refresh_and_banner(banner_to_use)
    print(f"\n{GREEN}--- {tool_name} ---{RESET}")
    print(f"{LIGHT_GRAY}Tip: {tip_message}{RESET}\n") # Display tip

    if not check_tool_installed(tool_name.split(' ')[0].lower()): # Check base command name
        print(f"{RED}Error: '{tool_name}' is NOT installed or not found in your system's PATH.{RESET}")
        print(f"{RED}Please install it using your OS package manager (e.g., 'sudo apt install {tool_name.split(' ')[0].lower()}') or from its official source.{RESET}")
        input(f"\n{CYAN}Press Enter to return to previous menu...{RESET}")
        return

    # Prompt for target, allowing flexibility for different tools
    target_prompt = ""
    if "nmap" in command_template or "masscan" in command_template or "rustscan" in command_template or "netdiscover" in command_template or "arp-scan" in command_template:
        target_prompt = "Enter target IP, range (e.g., 192.168.1.0/24), or domain: "
    elif "http" in command_template or "https" in command_template or "url" in command_template or "domain" in command_template:
        target_prompt = "Enter target URL (e.g., http://example.com) or domain: "
    elif "hydra" in command_template or "medusa" in command_template:
        target_prompt = "Enter target service/host (e.g., ssh://192.168.1.1): "
    elif "prowler" in command_template or "trivy" in command_template or "clair" in command_template:
        target_prompt = "Enter target (e.g., AWS account ID, image name, directory): "
    elif "bandit" in command_template or "semgrep" in command_template:
        target_prompt = "Enter target code directory or file: "
    else:
        target_prompt = "Enter target: " # Fallback for other/unknown types

    target = input(f"{YELLOW}{target_prompt}{RESET}")

    full_command = command_template.format(target=target)
    print(f"\n{BLUE}Executing command: {full_command}{RESET}\n")

    try:
        # Using subprocess.run with shell=True for convenience, output directly to terminal
        process = subprocess.run(full_command, shell=True, check=True, text=True, capture_output=False)
        print(f"\n{GREEN}--- {tool_name} scan completed. ---{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error executing {tool_name}: Command exited with code {e.returncode}{RESET}")
        print(f"{RED}Details: {e.stderr if e.stderr else 'No specific error output.'}{RESET}")
        print(f"{RED}Please review the command and target, and ensure the tool's dependencies are met.{RESET}")
    except Exception as e:
        print(f"{RED}An unexpected error occurred while running {tool_name}: {e}{RESET}")

    input(f"\n{CYAN}Press Enter to return to previous menu...{RESET}")

# Function to check and display status of common tools
def check_tool_status():
    refresh_and_banner(GENERIC_SUB_MENU_BANNER)
    print(f"\n{GREEN}--- Checking Scanner Tool Status ---{RESET}")
    print(f"{LIGHT_GRAY}Please wait, checking for common tools in your system's PATH...{RESET}\n")
    time.sleep(1) # Small delay for effect

    tools_to_check = {
        "Nmap": "nmap",
        "Masscan": "masscan",
        "RustScan": "rustscan",
        "Arp-scan": "arp-scan",
        "Netdiscover": "netdiscover",
        "OWASP ZAP (CLI)": "zap-cli", # Assuming zap-cli is used for CLI
        "Nikto": "nikto",
        "Wapiti": "wapiti",
        "Nuclei": "nuclei",
        "sqlmap": "sqlmap",
        "XSStrike": "xsstrike",
        "Dalfox": "dalfox",
        "Subfinder": "subfinder",
        "Amass": "amass",
        "Assetfinder": "assetfinder",
        "Knockpy": "knockpy",
        "WPScan": "wpscan",
        "JoomScan": "joomscan",
        "Droopescan": "droopescan",
        "Hydra": "hydra",
        "Medusa": "medusa",
        "Dirb": "dirb",
        "Gobuster": "gobuster",
        "FFuF": "ffuf",
        "Prowler": "prowler",
        "Trivy": "trivy",
        "Clair": "clairctl", # Assuming clairctl is the CLI for Clair
        "Bandit": "bandit",
        "Semgrep": "semgrep",
    }

    for display_name, command_name in tools_to_check.items():
        status_color = GREEN if check_tool_installed(command_name) else RED
        status_text = "INSTALLED" if check_tool_installed(command_name) else "NOT INSTALLED"
        print(f"  {display_name:<20}: {status_color}{status_text}{RESET}")
        if not check_tool_installed(command_name):
            print(f"    {LIGHT_GRAY}  -> Install '{command_name}' via apt/brew or its official source.{RESET}")

    print(f"\n{GREEN}--- Tool Status Check Complete ---{RESET}")
    input(f"\n{CYAN}Press Enter to return to Main Menu...{RESET}")


# Main menu loop
while True:
    refresh_and_banner(SCANNER_MAIN_BANNER)
    print(f"{CYAN}Made with <3 by ANS! - version 1.1{RESET}")
    print(f"{RED}╔══════════════════════════════════════════════════════╗")
    print(f"║{RESET} {CYAN}[!] This tool requires external scanners to be installed.{RED} ║")
    print(f"║{RESET} {CYAN}[!] Use option [11] to check installed tools.           {RED} ║")
    print(f"╚══════════════════════════════════════════════════════╝{RESET}")
    draw_box(left_menu, right_menu)
    print(f"\n{YELLOW}Select a category (1-11, or 'exit' to quit): {RESET}")
    choice = input().lower()

    if choice == "exit":
        refresh_and_banner(SCANNER_MAIN_BANNER) # Clear screen before exiting
        print(f"{BLUE}Exiting Scanning Multi-Tool. Goodbye!{RESET}")
        break
    elif choice.isdigit():
        choice_int = int(choice)

        if choice_int == 1: # Network & Port Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- Network & Port Scanners ---{RESET}")
                print(f"1. Nmap (Network Mapper)")
                print(f"2. Masscan")
                print(f"3. RustScan")
                print(f"4. Arp-scan")
                print(f"5. Netdiscover")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-5): {RESET}")

                if sub_choice == "1":
                    run_scanner("Nmap", "nmap {target}", "Versatile for host discovery, port scanning, OS detection.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("Masscan", "masscan {target} -p80,443", "Ultra-fast port scanner, use -p for ports.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "3":
                    run_scanner("RustScan", "rustscan -a {target} -p 22,80,443,8080", "Modern, fast port scanner. Pipes to Nmap by default.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "4":
                    run_scanner("Arp-scan", "sudo arp-scan --localnet", "Discover hosts on local network using ARP. Often needs sudo.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "5":
                    run_scanner("Netdiscover", "sudo netdiscover -r {target}", "Active/Passive ARP reconnaissance. Often needs sudo.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 2: # Web Vulnerability Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- Web Vulnerability Scanners ---{RESET}")
                print(f"1. OWASP ZAP (CLI)")
                print(f"2. Nikto")
                print(f"3. Wapiti")
                print(f"4. Nuclei")
                print(f"5. sqlmap")
                print(f"6. XSStrike")
                print(f"7. Dalfox")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-7): {RESET}")

                if sub_choice == "1":
                    run_scanner("OWASP ZAP (CLI)", "zap-cli scan -s all -t {target}", "Comprehensive web app scanner. Requires ZAP daemon/API running.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("Nikto", "nikto -h {target}", "Web server scanner for dangerous files, outdated software.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "3":
                    run_scanner("Wapiti", "wapiti {target}", "Black-box web app scanner, injects payloads.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "4":
                    run_scanner("Nuclei", "nuclei -u {target}", "Fast, template-based vulnerability scanner for various issues.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "5":
                    run_scanner("sqlmap", "sqlmap -u {target} --batch --random-agent --banner", "Automated SQL Injection and database takeover tool.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "6":
                    run_scanner("XSStrike", "xsstrike -u {target} --auto", "Sophisticated XSS scanner with WAF bypass capabilities.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "7":
                    run_scanner("Dalfox", "dalfox url {target}", "Fast and powerful XSS scanning tool.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 3: # Subdomain & Recon Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- Subdomain & Recon Scanners ---{RESET}")
                print(f"1. Subfinder")
                print(f"2. Amass")
                print(f"3. Assetfinder")
                print(f"4. Knockpy")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-4): {RESET}")

                if sub_choice == "1":
                    run_scanner("Subfinder", "subfinder -d {target}", "Fast subdomain discovery using various techniques.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("Amass", "amass enum -d {target}", "Advanced subdomain enumeration with active/passive recon.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "3":
                    run_scanner("Assetfinder", "assetfinder {target}", "Simple and fast tool to find domains and subdomains.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "4":
                    run_scanner("Knockpy", "knockpy {target}", "Python tool to enumerate subdomains. Often needs Python 2.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 4: # CMS & Specific App Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- CMS & Specific App Scanners ---{RESET}")
                print(f"1. WPScan")
                print(f"2. JoomScan")
                print(f"3. Droopescan")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-3): {RESET}")

                if sub_choice == "1":
                    run_scanner("WPScan", "wpscan --url {target}", "WordPress vulnerability scanner (core, plugins, themes).", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("JoomScan", "joomscan -u {target}", "Joomla vulnerability scanner.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "3":
                    run_scanner("Droopescan", "droopescan -u {target}", "Multi-CMS scanner (Drupal, Joomla, WordPress, Moodle).", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 5: # Authentication & Credential Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- Authentication & Credential Scanners ---{RESET}")
                print(f"1. Hydra")
                print(f"2. Medusa")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-2): {RESET}")

                if sub_choice == "1":
                    run_scanner("Hydra", "hydra {target}", "Fast network login cracker. Complex usage, requires wordlists.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("Medusa", "medusa {target}", "Speedy, parallel, modular login brute-forcer. Requires wordlists.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 6: # Content Discovery Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- Content Discovery Scanners ---{RESET}")
                print(f"1. Dirb")
                print(f"2. Gobuster")
                print(f"3. FFuF")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-3): {RESET}")

                if sub_choice == "1":
                    run_scanner("Dirb", "dirb {target}", "Web content scanner for hidden files/directories. Requires wordlist.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("Gobuster", "gobuster dir -u {target} -w /path/to/wordlist.txt", "Fast directory/file, DNS, VHost brute-forcer. Requires wordlist.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "3":
                    run_scanner("FFuF", "ffuf -u {target}/FUZZ -w /path/to/wordlist.txt", "Fast web fuzzer for content discovery. Requires wordlist.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 7: # Cloud & Container Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- Cloud & Container Scanners ---{RESET}")
                print(f"1. Prowler")
                print(f"2. Trivy")
                print(f"3. Clair")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-3): {RESET}")

                if sub_choice == "1":
                    run_scanner("Prowler", "prowler {target}", "AWS security assessment tool. Requires AWS credentials configured.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("Trivy", "trivy image {target}", "Container image, filesystem, repo vulnerability scanner (e.g., 'nginx:latest').", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "3":
                    run_scanner("Clair", "clairctl analyze {target}", "Container vulnerability analysis. Requires a running Clair instance.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 8: # Code Analysis (SAST) Scanners
            while True:
                refresh_and_banner(GENERIC_SUB_MENU_BANNER)
                print(f"\n{GREEN}--- Code Analysis (SAST) Scanners ---{RESET}")
                print(f"1. Bandit")
                print(f"2. Semgrep")
                print(f"0. Back to Main Menu")
                sub_choice = input(f"\n{YELLOW}Choose an option (0-2): {RESET}")

                if sub_choice == "1":
                    run_scanner("Bandit", "bandit -r {target}", "Python security linter for common security issues.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "2":
                    run_scanner("Semgrep", "semgrep --config 'p/all' {target}", "Multi-language static analysis for bugs and security flaws.", GENERIC_SUB_MENU_BANNER)
                elif sub_choice == "0":
                    break
                else:
                    print(f"{RED}Invalid selection. Please try again.{RESET}")
                time.sleep(0.5)

        elif choice_int == 9: # Other / Advanced Scanners (Placeholder)
            print(f"\n{GREEN}-- Other / Advanced Scanners (Coming Soon) --{RESET}")
            print(f"This section will feature more specialized or advanced scanning tools.")
            input(f"{CYAN}Press Enter to return to Main Menu...{RESET}")

        elif choice_int == 10: # Coming Soon... (Placeholder)
            print(f"\n{GREEN}-- Coming Soon... --{RESET}")
            print(f"More scanning categories and tools are under development!")
            input(f"{CYAN}Press Enter to return to Main Menu...{RESET}")

        elif choice_int == 11: # Check Tool Status
            check_tool_status()

        else:
            print(f"{RED}Invalid selection. Please try again.{RESET}")
    else:
        print(f"{RED}Invalid input. Please enter a number or 'exit'.{RESET}")
