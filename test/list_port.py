import subprocess

def get_connected_arduino_ports():
    # Command to list all connected Arduino boards
    command = ["arduino-cli", "board", "list"]
    
    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check for errors in execution
    if result.returncode != 0:
        print("Failed to execute command:", result.stderr)
        return []

    # Split the output into lines for processing
    lines = result.stdout.splitlines()

    output = []

    print(len(lines))
    
    for item in lines:
        for word in item.split():
            if word.startswith("/dev/"):
                output.append(word)
    
    return output
    # Port names will be collected in this list
    # port_names = []
    
    # # Parse each line after the header (assuming headers are always the first line)
    # for line in lines[1:]:
    #     parts = line.split()
    #     if len(parts) >= 4 and parts[2].startswith('Arduino'):  # Check if 'Arduino' is in the board name part
    #         port_names.append(parts[0])  # Append the port part which is the first element

    # return port_names

# Example usage
ports = get_connected_arduino_ports()
print("Connected Arduino Ports:", ports)