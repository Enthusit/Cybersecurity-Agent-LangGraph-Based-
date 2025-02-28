from executor import run_nmap, run_gobuster, run_ffuf, run_sqlmap

print(run_nmap("scanme.nmap.org"))
print(run_gobuster("scanme.nmap.org"))
print(run_ffuf("scanme.nmap.org"))
print(run_sqlmap("testphp.vulnweb.com"))
