import aci_get_data_functions as aci
if __name__ == "__main__":
    base_url = "https://your-apic-ip/api"
    username = "your-username"
    password = "your-password"
    interface_list = [ "1/1", "1/14", "1/15", "1/17"]
    node_list = ["1104", "1105"]
    pod_list = ["1"]

    headers = {
        'Content-Type': "application/json"
    }

    cookie = aci.apic_login (base_url, username, password)
    pod_int_data = aci.get_pod_int_data(pod_list, node_list, interface_list, base_url, headers, cookie, username, password)
    df_pod_int_data = aci.get_data_csv(pod_int_data, "POD_INT_DATA.csv")
