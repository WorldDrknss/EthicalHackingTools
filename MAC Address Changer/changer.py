#!/usr/bin/env python

import subprocess
import argparse

# Function to Get Arguments
def arguments():
    """
    Parses and returns command-line arguments for the MAC address changer.

    Returns:
        Namespace: An object containing the parsed command-line arguments:
            - interface (str): The network interface to change its MAC address.
            - mac (str): The new MAC address to assign to the interface.

    Raises:
        ArgumentError: If the required arguments are not provided.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address", required=True)
    parser.add_argument("-m", "--mac", dest="mac", help="New MAC address", required=True)
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options

# Function to Change MAC Address
def changer(interface, mac):
    """
    Changes the MAC address of a specified network interface.

    Args:
        interface (str): The name of the network interface (e.g., 'eth0').
        mac (str): The new MAC address to assign to the network interface.

    Returns:
        None
    """
    print("[+] Changing MAC address for " + interface + " to " + mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

def current(interface):
    """
    Prints the current MAC address of the specified network interface.

    Args:
        interface (str): The name of the network interface to check.

    Raises:
        subprocess.CalledProcessError: If the ifconfig command fails.
        IndexError: If the MAC address cannot be parsed from the ifconfig output.
    """
    ifconfigResults = subprocess.check_output(["ifconfig", interface])
    currentMAC = ifconfigResults.decode().split("ether")[1].split()[0]
    if currentMAC:
        print("[+] Current MAC address is " + currentMAC)
    else:
        print("[-] Could not read MAC address.")

# Main Function
options = arguments()
currentMAC = current(options.interface)
if currentMAC != options.mac:
    changer(options.interface, options.mac)