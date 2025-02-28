# 🔍 Cybersecurity Agent (LangGraph-Based)
This is an **automated penetration testing workflow** built with **LangGraph**, integrating **Nmap, Gobuster, FFUF, and SQLMap** to perform security scans on predefined test domains.

## 📌 Features
- ✅ **Automated Security Scans** (Nmap, Gobuster, FFUF, SQLMap)
- ✅ **Scope Enforcement** (Only allowed domains can be scanned)
- ✅ **Logging & Audit Reports** (Stored in `scan_log.txt`)
- ✅ **Results Saved in JSON** (`scan_report.json`)
- ✅ **Streamlit Dashboard** (View scan results visually)
- ✅ **Automated Tests with Pytest**

## 🛠 Installation
### 1️⃣ Clone the Repository
```bash
git clone <https://github.com/Enthusit/Cybersecurity-Agent-LangGraph-Based->
cd langgraph-cybersecurity-agent
```

### 2️⃣ Set Up Virtual Environment
```bash
python -m venv ai
source ai/bin/activate  # Mac/Linux
ai\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 How to Use
### 1️⃣ Run the Cybersecurity Agent (Manual)
```bash
python agent.py scanme.nmap.org
```
**This will:**
- Run **Nmap**, **Gobuster**, **FFUF**, and **SQLMap** on `scanme.nmap.org`
- Save results in `scan_report_scanme_nmap_org.json`
- Log all activities in `scan_log.txt`

### 2️⃣ Run the Streamlit Dashboard
```bash
streamlit run dashboard.py
```
**This will:**
- Provide a **web interface** to view previous scan results
- Allow users to start new scans by entering a domain

### 3️⃣ View Logs & Reports
#### 🔹 View Scan Logs
```bash
cat scan_log.txt
```
#### 🔹 View JSON Scan Report
```bash
cat scan_report_scanme_nmap_org.json
```

## 🧪 Running Tests
### Run Pytest to Ensure Everything Works
```bash
pytest test_agent.py
```
**Expected Output:**
```
======================= test session starts =======================
collected 5 tests

✅ test_allowed_targets PASSED
✅ test_nmap_execution PASSED
✅ test_gobuster_execution PASSED
✅ test_ffuf_execution PASSED
✅ test_sqlmap_execution PASSED
```

## 📂 Project Structure
```
langgraph-cybersecurity-agent/
│── agent.py               # Main LangGraph cybersecurity agent
│── dashboard.py           # Streamlit dashboard for scan results
│── executor.py            # Functions to run Nmap, Gobuster, FFUF, and SQLMap
│── test_agent.py          # Pytest test cases
│── requirements.txt       # Python dependencies
│── scan_log.txt           # Logs of all scan activities
│── scan_report.json       # JSON file storing scan results
│── README.md              # Documentation (this file)
```

## ⚠️ Legal Disclaimer
🚨 **This tool is for educational and authorized testing only.**
Unauthorized scanning of websites is **illegal**. Only use this tool on domains you have permission to test.

