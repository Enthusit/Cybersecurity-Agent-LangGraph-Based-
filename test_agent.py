import pytest
from agent import is_target_allowed
from executor import run_nmap, run_gobuster, run_ffuf, run_sqlmap

# ✅ Test Scope Enforcement
def test_allowed_targets():
    assert is_target_allowed("scanme.nmap.org") == True
    assert is_target_allowed("testphp.vulnweb.com") == True
    assert is_target_allowed("example.com") == True
    assert is_target_allowed("google.com") == False  # ❌ Google should be blocked

# ✅ Test Nmap Execution
def test_nmap_execution():
    target = "scanme.nmap.org"
    result = run_nmap(target)
    assert "PORT" in result or "open" in result  # ✅ Ensures Nmap found something

# ✅ Test Gobuster Execution
def test_gobuster_execution():
    target = "scanme.nmap.org"
    result = run_gobuster(target)
    assert "/index" in result or "/images" in result or "Status:" in result  # ✅ Ensures directories were found

# ✅ Test FFUF Execution
def test_ffuf_execution():
    target = "scanme.nmap.org"
    result = run_ffuf(target)
    assert "Status:" in result or "FUZZ" in result  # ✅ Ensures FFUF found something

# ✅ Test SQLMap Execution
def test_sqlmap_execution():
    target = "scanme.nmap.org"
    result = run_sqlmap(target)
    assert "sqlmap" in result.lower() or "testing" in result.lower()  # ✅ Ensures SQLMap ran
