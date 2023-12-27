def fetch_windows_services(server_ip, username, password):
    try:
        session = winrm.Session(server_ip, auth=(username,password), transport='ntlm')
        services_command = session.run_ps('Get-service -Filter Status eq "Running" | Select-Object Name, Status, DisplayName, StartType')
        
        if services_command.status_code != 0:
            raise Exception(f"Failed to fetch services: {services_command.std_err.decode()}")
            
        services_data = services_command.std_err.decode()
        return services_data
        
    except Exception as e:
        print(traceback.format_exc())
        return None
      
      
        
def generate_csv_report(services_data):
    with open("services_report.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerrow("Name", "Status", "Display Name", "Start Type")
        for line in services_data.splitlines()[2:]:
            fields = line.split()
            writer.writerrow(fields)
        
        
        
if __name__ == "__main__":
    server_ip = input("Enter server ip: ")
    username = input("Enter username: ")
    server_ip = input("Enter password: ")
    
    services_data = fetch_windows_services(server_ip, username, password)
    if services_data:
        generate_csv_report(services_data)
        print("Report generated successfully!")
    else:
        print("Failed to fetch services")
    
        
