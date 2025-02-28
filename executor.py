import subprocess
import time

def run_nmap(target, retries=3):
    """Run an Nmap scan with retry logic."""
    for attempt in range(retries):
        try:
            print(f"🛠 Running Nmap scan on {target} (Attempt {attempt+1}/{retries})...")
            result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True, timeout=30)
            if result.stdout:
                return result.stdout  # ✅ Successful scan
        except subprocess.TimeoutExpired:
            print(f"⚠️ Nmap timed out on attempt {attempt+1}. Retrying...")
        except Exception as e:
            print(f"❌ Nmap failed: {str(e)}")
    
    return f"❌ Nmap scan failed after {retries} attempts."

def run_gobuster(target, wordlist="fast_wordlist.txt", retries=3):
    """Run a Gobuster scan with retry logic."""
    for attempt in range(retries):
        try:
            print(f"🛠 Running Gobuster scan on {target} (Attempt {attempt+1}/{retries})...")
            result = subprocess.run(
                ["gobuster", "dir", "-u", target, "-w", wordlist, "-t", "10", "--timeout", "5s"], 
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                return result.stdout  # ✅ Successful scan
        except subprocess.TimeoutExpired:
            print(f"⚠️ Gobuster timed out on attempt {attempt+1}. Retrying...")
        except Exception as e:
            print(f"❌ Gobuster failed: {str(e)}")
    
    return f"❌ Gobuster scan failed after {retries} attempts."

def run_ffuf(target, wordlist="fast_wordlist.txt", retries=3):
    """Run FFUF for subdomain fuzzing with better filtering."""
    for attempt in range(retries):
        try:
            print(f"🔎 Running FFUF scan on {target} (Attempt {attempt+1}/{retries})...")
            result = subprocess.run(
                ["ffuf", "-u", f"http://{target}/FUZZ", "-w", wordlist, "-mc", "200,301", 
                 "-fs", "1256"],  # ✅ Filter responses with size 1256 (avoid license text)
                capture_output=True, text=True
            )
            if result.stdout:
                return result.stdout  # ✅ Successful scan
        except Exception as e:
            print(f"❌ FFUF failed on attempt {attempt+1}: {str(e)}")

    return f"❌ FFUF scan failed after {retries} attempts."


def run_sqlmap(target, retries=3):
    """Run SQLMap with advanced bypass techniques."""
    for attempt in range(retries):
        try:
            print(f"💉 Running SQLMap scan on {target} (Attempt {attempt+1}/{retries})...")
            result = subprocess.run(
                ["sqlmap", "-u", f"http://{target}", "--batch", "--level=5", "--risk=3", 
                 "--random-agent", "--tamper=between,space2comment", "--forms", "--crawl=3"], 
                capture_output=True, text=True
            )
            if result.stdout:
                return result.stdout  # ✅ Successful scan
        except Exception as e:
            print(f"❌ SQLMap failed on attempt {attempt+1}: {str(e)}")

    return f"❌ SQLMap scan failed after {retries} attempts."

