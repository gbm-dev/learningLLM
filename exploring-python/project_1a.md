# Practical Project 1: IPAM (IP Address Management) Tool - Foundation

## Project Overview
In this project, you will build the foundation for an IP Address Management (IPAM) tool using Pydantic for data validation and a command-line interface for user interaction. This project will serve as a stepping stone towards the more comprehensive Network Management and Automation Platform in the capstone project.

## Project Goals
1. Create Pydantic models for IP addresses, subnets, and network devices
2. Implement a command-line interface for IPAM operations
3. Validate user input for IP-related data using Pydantic
4. Handle and display validation errors
5. Implement basic IPAM functionality (add/view/delete IP addresses and subnets)

## Project Description
You will create an "IPAM Tool" that can manage IP addresses and subnets. The application will:
1. Allow users to add, view, and delete IP addresses and subnets
2. Validate IP address and subnet input
3. Perform basic subnet calculations
4. Store data in-memory (to be extended to database storage in the capstone)

## Implementation Steps

### 1. Set up the project
- Create a new Python file named `ipam_tool.py`
- Import necessary modules (including Pydantic)

### 2. Define Pydantic models
Create models for IP addresses, subnets, and network devices:

```python
from pydantic import BaseModel, IPvAnyAddress, constr
from typing import List, Optional
from ipaddress import ip_network

class IPAddress(BaseModel):
    address: IPvAnyAddress
    description: Optional[str] = None

class Subnet(BaseModel):
    network: str
    description: Optional[str] = None

    @validator('network')
    def validate_network(cls, v):
        try:
            ip_network(v)
        except ValueError:
            raise ValueError('Invalid network address')
        return v

class NetworkDevice(BaseModel):
    hostname: constr(min_length=1, max_length=100)
    ip_address: IPvAnyAddress
    device_type: str
```

### 3. Implement core IPAM functionality
Create functions for:
- Adding IP addresses and subnets
- Viewing IP addresses and subnets
- Deleting IP addresses and subnets
- Basic subnet calculations (e.g., available IPs, broadcast address)

### 4. Implement the command-line interface
- Create a main loop that presents IPAM options to the user
- Implement functions to gather input for each IPAM operation

### 5. Validate data and handle errors
- Use Pydantic models to validate user input
- Catch and handle ValidationError exceptions
- Display helpful error messages or success confirmations

### 6. (Optional) Implement basic IP allocation logic
- Add functionality to allocate IP addresses from a subnet
- Track used and available IP addresses within subnets

## Example Code Structure

```python
import ipaddress
from pydantic import BaseModel, IPvAnyAddress, validator
from typing import List, Optional

# Pydantic models (as defined above)

class IPAMTool:
    def __init__(self):
        self.ip_addresses = []
        self.subnets = []

    def add_ip_address(self, address: str, description: Optional[str] = None):
        try:
            ip = IPAddress(address=address, description=description)
            self.ip_addresses.append(ip)
            print(f"IP address {address} added successfully.")
        except ValidationError as e:
            print(f"Error adding IP address: {e}")

    def add_subnet(self, network: str, description: Optional[str] = None):
        try:
            subnet = Subnet(network=network, description=description)
            self.subnets.append(subnet)
            print(f"Subnet {network} added successfully.")
        except ValidationError as e:
            print(f"Error adding subnet: {e}")

    def view_ip_addresses(self):
        for ip in self.ip_addresses:
            print(f"IP: {ip.address}, Description: {ip.description}")

    def view_subnets(self):
        for subnet in self.subnets:
            print(f"Network: {subnet.network}, Description: {subnet.description}")

    # Add more methods for delete operations and subnet calculations

def main():
    ipam = IPAMTool()
    while True:
        print("\nIPAM Tool Menu:")
        print("1. Add IP Address")
        print("2. Add Subnet")
        print("3. View IP Addresses")
        print("4. View Subnets")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            address = input("Enter IP address: ")
            description = input("Enter description (optional): ")
            ipam.add_ip_address(address, description)
        elif choice == '2':
            network = input("Enter subnet (e.g., 192.168.1.0/24): ")
            description = input("Enter description (optional): ")
            ipam.add_subnet(network, description)
        elif choice == '3':
            ipam.view_ip_addresses()
        elif choice == '4':
            ipam.view_subnets()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
```

## Expected Outcome
Upon completion, you will have a functioning command-line IPAM tool that demonstrates practical use of Pydantic for IP address and subnet validation. This project will reinforce your understanding of:
- Creating and using Pydantic models for network-related data
- Handling user input and validation errors for IP addresses and subnets
- Applying constraints and custom validators to fields
- Basic IPAM operations and data management

## Bonus Challenges
1. Implement IP address status (e.g., available, reserved, in-use)
2. Add VLAN support to subnets
3. Implement a basic conflict detection system for IP addresses
4. Add an option to export IPAM data to CSV or JSON format
5. Implement a simple network device inventory system

This project sets a solid foundation for the IPAM component of your capstone project while reinforcing the Pydantic concepts covered in the first three chapters of the course. It provides hands-on experience with IP address validation and management, which will be crucial for the more advanced features in the final Network Management and Automation Platform.