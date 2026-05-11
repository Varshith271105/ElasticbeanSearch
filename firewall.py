import requests, csv, subprocess

# Download IP blocklist
data = requests.get(
    "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
).text

# Delete old firewall rule
subprocess.run([
    "PowerShell", "-Command",
    'netsh advfirewall firewall delete rule name="BadIP"'
])

# Read CSV and block IPs
for row in csv.reader(filter(lambda x: not x.startswith("#"), data.splitlines())):
    ip = row[1]

    if ip != "dst_ip":
        print("Blocking:", ip)

        subprocess.run([
            "PowerShell", "-Command",
            f"netsh advfirewall firewall add rule name='BadIP' dir=out action=block remoteip={ip}"
        ])
