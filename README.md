# Cisco ACI Interface Data Retrieval

This Python script is designed to retrieve operational data from a Cisco Application Policy Infrastructure Controller (APIC). It can fetch information about Ethernet interfaces, including operational state, speed, mode, administrative state, description, MAC addresses, IP addresses, and associated End Point Groups (EPGs).

## Prerequisites

Before running this script, ensure you have the following prerequisites:

- Python 3.x installed
- Required Python libraries installed (requests, json, pandas)
- Access to a Cisco APIC with appropriate permissions
- APIC IP address and login credentials

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/samaelsan/ACI-Get-Interface-Data.git
   cd ACI-Get-Interface-Data

2. Install the required Python libraries if not already installed:

   ```bash
   pip install requests pandas
   
3. Open the ACI_GET_INT_DATA.py script and replace the placeholders for base_url, username, and password with your APIC's information:

   ```Python
   base_url = "https://your-apic-ip/api"
   username = "your-username"
   password = "your-password"
4. Customize the list of Ethernet interfaces, nodes, and pods in the script as needed:

   ```Python
   interface_list = ["1/1", "1/14", "1/15", "1/17"]
   node_list = ["1104", "1105"]
   pod_list = ["1"]

5. Run the script:
   
   ```bash
   python ACI_GET_INT_DATA.py
   
The script will fetch data from the APIC and save it to a CSV file named POD_INT_DATA.csv.
