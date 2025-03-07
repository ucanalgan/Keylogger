# This script scans a target IP address for open ports within a given range.
# It uses threading to speed up the process.
#
# The script takes three arguments: the target IP address, the start port, and
# the end port. If these arguments are not supplied, the script will prompt the
# user for them.

import socket
from datetime import datetime
import sys
import threading

# This function scans a single port on the target IP address.
def scan_port(target, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set the default timeout to 1 second
        socket.setdefaulttimeout(1)
        # Attempt to connect to the target port
        result = sock.connect_ex((target, port))
        if result == 0:
            # If the connection is successful, the port is open
            try:
                # Get the service name associated with the port
                service = socket.getservbyport(port)
                # Send a HEAD request to the target port
                sock.send(b'HEAD / HTTP/1.1\r\n\r\n')
                # Get the banner returned by the target
                banner = sock.recv(1024).decode().strip()
            except:
                # If there is an error, set the service name to "Unknown service"
                # and the banner to "No banner"
                service = "Unknown service"
                banner = "No banner"
            # Print the open port and its associated service and banner
            print(f"Port {port}: Open ({service}) - {banner}")
        # Close the socket
        sock.close()
    except Exception as e:
        # If there is an error, print it
        print(f"Error scanning port {port}: {e}")

# This function scans a range of ports on the target IP address.
def scan_ports(target, start_port, end_port):
    print(f"Scanning target: {target}")
    print(f"Time started: {str(datetime.now())}")
    print(f"Scanning ports from {start_port} to {end_port}")

    # Create a list to hold the threads
    threads = []
    # Iterate over the range of ports
    for port in range(start_port, end_port + 1):
        # Create a thread for each port
        thread = threading.Thread(target=scan_port, args=(target, port))
        # Add the thread to the list
        threads.append(thread)
        # Start the thread
        thread.start()

    # Iterate over the threads and join them
    for thread in threads:
        thread.join()

    print(f"Time finished: {str(datetime.now())}")

if __name__ == "__main__":
    # If the script is run from the command line, get the arguments
    if len(sys.argv) == 4:
        target = sys.argv[1]
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    # Otherwise, prompt the user for the arguments
    else:
        target = input("Enter the target IP address: ")
        start_port = int(input("Enter the start port: "))
        end_port = int(input("Enter the end port: "))
    # Call the scan_ports function with the arguments
    scan_ports(target, start_port, end_port)