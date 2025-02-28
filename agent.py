import sys
import json
import datetime
import os
from langgraph.graph import StateGraph
from executor import run_nmap, run_gobuster, run_ffuf, run_sqlmap

class ScanState(dict):
    """State schema to pass data between tasks."""

# ✅ Logging Function
log_file = "scan_log.txt"

def log_action(action):
    """Write actions to a log file."""
    with open(log_file, "a") as log:
        log.write(f"{datetime.datetime.now()} - {action}\n")

# ✅ Define Allowed Targets
ALLOWED_TARGETS = ["scanme.nmap.org", "testphp.vulnweb.com", "example.com"]

def is_target_allowed(target):
    """Check if the target is within the allowed scope."""
    return target in ALLOWED_TARGETS

def task_nmap(state: ScanState):
    """Runs an Nmap scan and returns results."""
    target = state["target"]
    log_action(f"Running Nmap scan on {target}")
    result = run_nmap(target)

    open_ports = []
    for line in result.split("\n"):
        if "/tcp" in line and "open" in line:
            port = line.split("/")[0].strip()
            open_ports.append(port)

    print(f"🔍 Found open ports: {open_ports}")
    
    # ✅ Store `open_ports` in state
    state["open_ports"] = open_ports
    state["results"]["nmap"] = {
        "open_ports": open_ports,
        "full_output": result
    }
    
    log_action(f"Nmap found open ports: {', '.join(open_ports) if open_ports else 'None'}")
    
    # ✅ Schedule additional scans if port 80 is open
    if "80" in open_ports:
        state["next_tasks"].extend([
            {"type": "gobuster", "target": target},
            {"type": "ffuf", "target": target},
            {"type": "sqlmap", "target": target}
        ])

    return state

def task_gobuster(state: ScanState):
    """Runs a Gobuster scan and returns results."""
    target = state["target"]
    log_action(f"Running Gobuster scan on {target}")
    result = run_gobuster(target)
    
    print(f"📂 Gobuster Results:\n{result}")
    state["results"]["gobuster"] = {
        "directories": [line for line in result.split("\n") if "(Status:" in line],
        "full_output": result
    }
    
    log_action(f"Gobuster completed. Directories: {state['results']['gobuster']['directories']}")
    return state

def task_ffuf(state: ScanState):
    """Runs an FFUF scan and returns results."""
    target = state["target"]
    log_action(f"Running FFUF scan on {target}")
    result = run_ffuf(target)
    
    print(f"🔎 FFUF Results:\n{result}")
    state["results"]["ffuf"] = {
        "subdomains": [line for line in result.split("\n") if "(Status:" in line],
        "full_output": result
    }
    
    log_action(f"FFUF completed. Subdomains: {state['results']['ffuf']['subdomains']}")
    return state

def task_sqlmap(state: ScanState):
    """Runs an SQLMap scan and returns results."""
    target = state["target"]
    log_action(f"Running SQLMap scan on {target}")
    result = run_sqlmap(target)

    print(f"💉 SQLMap Results:\n{result}")
    state["results"]["sqlmap"] = {
        "vulnerabilities": ["Potential SQLi" if "sqlmap identified" in result else "None"],
        "full_output": result
    }
    
    log_action(f"SQLMap completed. SQL vulnerabilities: {state['results']['sqlmap']['vulnerabilities']}")
    return state

# ✅ Create LangGraph Workflow
workflow = StateGraph(ScanState)
workflow.add_node("nmap_scan", task_nmap)
workflow.add_node("gobuster_scan", task_gobuster)
workflow.add_node("ffuf_scan", task_ffuf)
workflow.add_node("sqlmap_scan", task_sqlmap)
workflow.set_entry_point("nmap_scan")

# ✅ Add Conditional Edges (Runs Gobuster, FFUF, and SQLMap if Port 80 is Open)
workflow.add_conditional_edges(
    "nmap_scan",
    lambda state: [
        ("gobuster_scan", state),
        ("ffuf_scan", state),
        ("sqlmap_scan", state)
    ] if "80" in state["results"]["nmap"]["open_ports"] else []
)

# ✅ Compile the Agent
agent = workflow.compile()

# ✅ Accept domain as command-line argument
if len(sys.argv) > 1:
    target = sys.argv[1].strip()
else:
    target = input("🔹 Enter the target domain/IP: ").strip()

if not is_target_allowed(target):
    print("⛔ Target is not allowed! Please enter a valid test domain.")
    exit(1)  

print(f"🚀 Starting security scan on {target}...\n")
log_action(f"Starting scan on {target}")

# ✅ Start with an Nmap Task
scan_results = {
    "target": target,
    "start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "results": {}
}

# ✅ Run all security tools and log each step
state = {"target": target, "results": {}, "next_tasks": []}
state = task_nmap(state)

if "gobuster_scan" in workflow.nodes and "80" in state["open_ports"]:
    state = task_gobuster(state)

if "ffuf_scan" in workflow.nodes and "80" in state["open_ports"]:
    state = task_ffuf(state)

if "sqlmap_scan" in workflow.nodes and "80" in state["open_ports"]:
    state = task_sqlmap(state)

scan_results["results"] = state["results"]
scan_results["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ✅ Save results in JSON format
json_report_filename = f"scan_report_{target.replace('.', '_')}.json"
with open(json_report_filename, "w") as json_report_file:
    json.dump(scan_results, json_report_file, indent=2)

log_action(f"Scan completed for {target}. Results saved to {json_report_filename}")
print(f"\n📝 Scan completed! Results saved to {json_report_filename}")
