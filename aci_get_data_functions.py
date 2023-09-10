import requests
import json
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re

def apic_login (base_url, username, password):
    try:
        login_url = f"{base_url}/aaaLogin.json"
        payload = {
            "aaaUser": {
                "attributes": {
                    "name": f"{username}",
                    "pwd": f"{password}"
                }
            } 
        }
        headers = {
            'Content-Type': "application/json"
        }
        login_req = requests.post(login_url, data = json.dumps(payload), headers = headers, verify = False)
        login_req_json = login_req.json ()
        login_req.raise_for_status()
        token = login_req_json["imdata"][0]["aaaLogin"]["attributes"]["token"]    
        cookie = {}
        cookie ["APIC-cookie"] = token
        return cookie
    except Exception as err:
        print(f"An unexpecter error was generated: {err}")


def get_oper_data (base_url, interface, node, pod, headers, cookie):
    try:
        oper_data = dict()
        oper_data_url = f"{base_url}/node/mo/topology/pod-{pod}/node-{node}/sys/phys-[eth{interface}].json?query-target=children&target-subtree-class=ethpmPhysIf"
        oper_data_req = requests.get (oper_data_url, headers = headers, cookies = cookie, verify = False)
        oper_data_req_json = oper_data_req.json()
        oper_data_req.raise_for_status()                
        if oper_data_req_json["imdata"]:
            oper_data["oper_state"] = oper_data_req_json["imdata"][0]["ethpmPhysIf"]["attributes"]["operSt"]
            oper_data["oper_speed"] = oper_data_req_json["imdata"][0]["ethpmPhysIf"]["attributes"]["operSpeed"]
            oper_data["oper_mode"] = oper_data_req_json["imdata"][0]["ethpmPhysIf"]["attributes"]["operMode"]
        else:
            oper_data["oper_state"] = "N/A"
            oper_data["oper_speed"] = "N/A"
            oper_data["oper_mode"] = "N/A"      
        return oper_data
    except Exception as err:
        if oper_data_req_json["imdata"][0]["error"]["attributes"]["code"] == "403":
            oper_data = {}
            return oper_data           
        else:
            print (f"An unexpecter error was generated: {err}")

def get_phys_if_data (base_url, interface, node, pod, headers, cookie):
    try:
        phys_if_data = dict()
        phys_if_data_url = f"{base_url}/node/mo/topology/pod-{pod}/node-{node}/sys/phys-[eth{interface}].json"
        phys_if_data_req = requests.get (phys_if_data_url, headers = headers, cookies = cookie, verify = False)
        phys_if_data_req_json = phys_if_data_req.json ()
        phys_if_data_req.raise_for_status()        
        if phys_if_data_req_json["imdata"]:
            phys_if_data["admin_state"] = phys_if_data_req_json["imdata"][0]["l1PhysIf"]["attributes"]["adminSt"]
            phys_if_data["description"] = phys_if_data_req_json["imdata"][0]["l1PhysIf"]["attributes"]["descr"]
        else:
            phys_if_data["admin_state"] = "N/A"
            phys_if_data["description"] = "N/A"
        if phys_if_data["description"] == "":
            phys_if_data["description"] = "N/A"    
        return phys_if_data
    except Exception as err:
        if phys_if_data_req_json["imdata"][0]["error"]["attributes"]["code"] == "403":
            phys_if_data = {}
            return (phys_if_data)             
        else:
            print (f"An unexpecter error was generated: {err}")

def get_mac_address (base_url, interface, node, pod, headers, cookie):
    try:
        mac_address = dict()
        mac_address_url = f'{base_url}/node/mo/topology/pod-{pod}/node-{node}/sys.json?query-target=subtree&target-subtree-class=epmMacEp&query-target-filter=eq(epmMacEp.ifId,"eth{interface}")'
        mac_address_req = requests.get (mac_address_url, headers = headers, cookies = cookie, verify = False)
        mac_address_req_json = mac_address_req.json ()
        mac_address_req.raise_for_status()        
        mac_address_list = list()
        if mac_address_req_json["imdata"]:
            for no_endpoint in range (int(mac_address_req_json["totalCount"])):
                mac_address_list.append(mac_address_req_json["imdata"][no_endpoint]["epmMacEp"]["attributes"]["addr"])
            mac_address["MAC"] = mac_address_list            
        else:
            mac_address["MAC"] = "N/A"
        return mac_address
    except Exception as err:
        if mac_address_req_json["imdata"][0]["error"]["attributes"]["code"] == "403":
            mac_address = {}
            return (mac_address)             
        else:
            print (f"An unexpecter error was generated: {err}")

def get_ip_address (base_url, interface, node, pod, headers, cookie):
    try:
        ip_address = dict()
        ip_address_url = f'{base_url}/node/mo/topology/pod-{pod}/node-{node}/sys.json?query-target=subtree&target-subtree-class=epmIpEp&query-target-filter=eq(epmIpEp.ifId,"eth{interface}")'
        ip_address_req = requests.get (ip_address_url, headers = headers, cookies = cookie, verify = False)
        ip_address_req_json = ip_address_req.json ()  
        ip_address_req.raise_for_status()       
        ip_address_list = list()
        if ip_address_req_json["imdata"]:
            for no_endpoint in range (int(ip_address_req_json["totalCount"])):
                ip_address_list.append(ip_address_req_json["imdata"][no_endpoint]["epmIpEp"]["attributes"]["addr"])
            ip_address["IP"] = ip_address_list
        else:
            ip_address["IP"] = "N/A"
        return ip_address
    except Exception as err:
        if ip_address_req_json["imdata"][0]["error"]["attributes"]["code"] == "403":
            ip_address = {}
            return (ip_address)             
        else:
            print (f"An unexpecter error was generated: {err}")

def get_epg (base_url, interfaz, node, pod, headers, cookie):
    try:
        epg = dict()
        epg_list = list()
        epg_url = f"{base_url}/node/mo/topology/pod-{pod}/node-{node}/sys/phys-[eth{interfaz}].json?rsp-subtree-include=full-deployment&target-node=all&target-path=l1EthIfToEPg"
        epg_list_req = requests.get (epg_url, headers = headers, cookies = cookie, verify = False)
        epg_list_req_json = epg_list_req.json()
        epg_list_req.raise_for_status()        
        epg_pattern = re.compile(r"tn-(?P<TENANT>\S+)\/ap-(?P<APP_PROF>\S+)\/epg-(?P<EPG>\S+)")
        for no_endpoint in range (int(epg_list_req_json["imdata"][0]["l1PhysIf"]["children"][0]["pconsCtrlrDeployCtx"]["attributes"]["count"])):
            ctxDn = epg_list_req_json["imdata"][0]["l1PhysIf"]["children"][0]["pconsCtrlrDeployCtx"]["children"][no_endpoint]["pconsResourceCtx"]["attributes"]["ctxDn"]
            epg_match = epg_pattern.search(ctxDn)
            epg_list.append(epg_match.group("EPG"))
        epg["EPG"] = epg_list
        return epg
    except KeyError:
        epg["EPG"] = "N/A"
        return epg   
    except Exception as err:
        if epg_list_req_json["imdata"][0]["error"]["attributes"]["code"] == "403":
            epg = {}
            return (epg)             
        else:
            print (f"An unexpecter error was generated: {err}")  


def get_int_data (base_url, interface, node, pod, headers, cookie, username, password):
    interfaces = dict()
    try:
        oper_data = get_oper_data (base_url, interface, node, pod, headers, cookie)
        phys_if_data = get_phys_if_data (base_url, interface, node, pod, headers, cookie)
        mac_address = get_mac_address (base_url, interface, node, pod, headers, cookie)
        ip_address = get_ip_address (base_url, interface, node, pod, headers, cookie)
        epg = get_epg (base_url, interface, node, pod, headers, cookie)
        if bool(oper_data) == False | bool(phys_if_data) == False | bool(mac_address) == False | bool(ip_address) == False | bool(epg) == False:
                print ("Invalid Token. Generating...")
                cookie = apic_login (base_url, username, password)
                print ("Token Generated. Retrying...")
        else:
            data_int = oper_data | phys_if_data | mac_address | ip_address | epg
            interfaces[f"eth {interface}"] = data_int
        return interfaces
    except Exception as err:
        print (f"An unexpecter error was generated: {err}")

def get_pod_int_data(pod_list, node_list, interface_list, base_url, headers, cookie, username, password):
    try:
        pod_data = dict()
        for pod in pod_list:    
            leaf_list = list()
            for node in node_list:
                leaf_dict = dict()
                int_data = list()
                for interface in interface_list:
                    int_data.append(get_int_data (base_url, interface, node, pod, headers, cookie, username, password))
                leaf_dict [f"Leaf {node}"] = int_data
                leaf_list.append(leaf_dict)
            pod_data[f"POD {pod}"] = leaf_list   
        return pod_data
    except Exception as err:
        print (f"An unexpecter error was generated: {err}")


def get_data_csv (data, csv_name):
    try:
        pod_index = list()
        leaf_index = list()
        int_index = list()
        data_interface = list()
        ind = [pod_index, leaf_index, int_index]
        for pod, pod_value in data.items():
            for leaf_no in range(0, len(pod_value)):
                current_leaf = list(pod_value[leaf_no].keys())[0]
                leaf_value = pod_value[leaf_no][current_leaf]
                for interface_no in range(0, len(leaf_value)):  
                    current_interface = list(leaf_value[interface_no].keys())[0] 
                    interface_value = leaf_value[interface_no][current_interface]          
                    pod_index.append(pod)
                    leaf_index.append(current_leaf)
                    int_index.append(current_interface)
                    data_int_list = list()
                    data_int_list.append(interface_value["oper_state"])
                    data_int_list.append(interface_value["oper_speed"])
                    data_int_list.append(interface_value["oper_mode"])
                    data_int_list.append(interface_value["admin_state"])
                    data_int_list.append(interface_value["description"])
                    data_int_list.append("N/A" if interface_value["MAC"] == "N/A" else ", ".join(interface_value["MAC"]))
                    data_int_list.append("N/A" if interface_value["IP"] == "N/A" else ", ".join(interface_value["IP"]))
                    data_int_list.append("N/A" if interface_value["EPG"] == "N/A" else ", ".join(interface_value["EPG"]))
                    data_interface.append(data_int_list)
        df_multi_index = pd.DataFrame (data_interface, index=ind, columns=["oper_state", "oper_speed", "oper_mode", "admin_state", "description", "MAC", "IP", "EPG"])
        df_multi_index.to_csv(csv_name)
        return df_multi_index   
    except Exception as err:
        print (f"An unexpecter error was generated: {err}")         
