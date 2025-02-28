import streamlit as st
import json
import glob
import os

# ✅ Page Title
st.title("🔍 Cybersecurity Scan Dashboard")
st.write("View Nmap, Gobuster, FFUF, and SQLMap results in real-time!")

# ✅ Load the latest scan report
scan_files = glob.glob("scan_report_*.json")
if not scan_files:
    st.warning("No scan reports found. Run a scan first!")
else:
    latest_scan = max(scan_files, key=os.path.getctime)
    st.write(f"📄 **Latest Scan Report: {latest_scan}**")
    
    with open(latest_scan, "r") as file:
        scan_data = json.load(file)
    
    # ✅ Show Scan Target
    st.subheader(f"🎯 Target: {scan_data['target']}")
    st.write(f"**Scan started:** {scan_data.get('start_time', 'N/A')}")
    st.write(f"**Scan finished:** {scan_data.get('end_time', 'N/A')}")

    # ✅ Display Nmap Results
    if "nmap" in scan_data["results"]:
        st.subheader("📌 Nmap Scan Results")
        st.text(scan_data["results"]["nmap"]["full_output"])

    # ✅ Display Gobuster Results
    if "gobuster" in scan_data["results"]:
        st.subheader("📂 Gobuster Scan Results")
        gobuster_lines = scan_data["results"]["gobuster"]["full_output"].split("\n")
        for line in gobuster_lines:
            if "(Status:" in line:
                st.write(f"✅ **{line.strip()}**")

# ✅ Run a New Scan
st.subheader("⚡ Run a New Scan")
target = st.text_input("Enter a target domain/IP (e.g., scanme.nmap.org)")

if st.button("Start Scan"):
    if target:
        st.write(f"🚀 Running scan on {target}...")
        
        # ✅ Run `agent.py` with the selected target (No manual input needed)
        os.system(f"python agent.py {target}")
        
        st.success("✅ Scan completed! Refresh to see new results.")
    else:
        st.error("⛔ Please enter a valid domain or IP!")
