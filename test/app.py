import tkinter as tk
import os
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


def execute_function():
    wifi = str(entry1.get())
    password = str(entry2.get())

    devui = str(entry3.get())
    appkey = str(entry4.get())

    print("executed")

    content = """

    #include \"Arduino.h\"
    #include <WiFi.h>
    #include <HTTPClient.h>

    #include <SoftwareSerial.h>


    // Change these setting

    // from chirpstack
    #define DEVEUI \""""

    content += devui 

    content += """\"
#define APPKEY \""""
    content += appkey
    content += """\"
    //configure wifi
    const char* ssid = \""""
    content += wifi
    content += """\"; // Your WiFi SSID
    const char* password = \""""
    content += password
    content += """\"; // Your WiFi password


    // optional, may change for customia

    // power setting
    #define POWER "20"
    const long interval = 5 * 60 * 1000;       // Interval at which to rejoin (5 minutes)



    // DO NOT CHANGE FOLLOWING SETTINGS

    // accoding to chirpstack manual, just set it to 0000000000000000
    #define APPEUI "0000000000000000"
    // SoftwareSerial to RX & TX of fall sensor
    #define RX_Pin D2
    #define TX_Pin D3
    // Define the RX and TX pins for SoftwareSerial for lorawan
    const int RX_PIN = D5; // RX is D5, not D4
    const int TX_PIN = D4; // TX is D4, not D5


    unsigned long previousMillis = 0;  // Stores the last time the join function executed
    SoftwareSerial mySerial(RX_PIN, TX_PIN);





    const unsigned char DevID_buff[10] = {0x53, 0x59, 0x02, 0xA1, 0x00, 0x01, 0x0F, 0x5F, 0x54, 0x43};
    const unsigned char turn_on[10] = {0x53, 0x59, 0x83, 0x00, 0x00, 0x01, 0x01, 0x31, 0x54, 0x43};
    const unsigned char query_fall[10] = {0x53, 0x59, 0x83, 0x81, 0x00, 0x01, 0x0F, 0xC0, 0x54, 0x43};
    unsigned char receive[10] = {0x53, 0x59, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x54, 0x43};

    // This function send command to the WioE5
    void SendCommand(String command) {
    mySerial.println(command);

    // Print the sent command to the Serial Monitor for debugging
    Serial.print("Sent: ");
    Serial.println(command);

    // Give some time for the Wio-E5 to respond
    delay(2000);

    // Check if there is any data available to read from the SoftwareSerial port
    if (mySerial.available()) {
        // Buffer to hold incoming data
        static char buffer[256];
        static int index = 0;
        
        // Read available characters
        while (mySerial.available() && index < sizeof(buffer) - 1) {
        buffer[index++] = mySerial.read();
        }
        
        // Null-terminate the string
        buffer[index] = '\\0';

        // Print the received response to the Serial Monitor
        Serial.print("Received: ");
        Serial.println(buffer);

        // Reset buffer index for next message
        index = 0;
    }

    // Wait for a while before sending the next command
    delay(1000);
    }

    void JoinNetwork() {
    // reset all settings
    SendCommand("AT+RESET");
    // set power
    SendCommand("AT+POWER=" POWER);
        // Connection Configuration
    SendCommand("AT+MODE=LWOTAA");
    SendCommand("AT+DR=AS923");
    SendCommand("AT+CH=NUM,0-2");
    SendCommand("AT+CLASS=A");
    SendCommand("AT+PORT=8");
    SendCommand("AT+ID=DevEui," DEVEUI);
    SendCommand("AT+ID=AppEui," APPEUI);
    SendCommand("AT+KEY=APPKEY," APPKEY);

        // Not sure whether these 2 lines are needed
    SendCommand("AT+CH=0,923200000,DR0,DR5");  // Channel 0 at 923.2 MHz
    SendCommand("AT+CH=1,923400000,DR0,DR5");  // Channel 1 at 923.4 MHz

    // join lorawan
    SendCommand("AT+JOIN");

        // give some time for the sensor to join
        delay(10000);
    }

    void sendPostRequest() {
        if (WiFi.status() == WL_CONNECTED) {
            HTTPClient http;

            http.begin("http://10.0.0.225:12082/fall"); // Specify the URL
            http.addHeader("Content-Type", "application/json"); // Optional header

            // Send the POST request
            int httpResponseCode = http.POST("");

            // Check for the response
            if (httpResponseCode > 0) {
                String response = http.getString();
                Serial.println(httpResponseCode);
                Serial.println(response);
            } else {
                Serial.print("Error on sending POST: ");
                Serial.println(httpResponseCode);
            }

            http.end(); // Free resources
        }
    }

    int x;
    int y;

    int state;


    void parseMessage(unsigned char *message) 
    {
    unsigned char category = message[2];
    Serial.print("Category: ");
    Serial.println(category, HEX);
    unsigned char command = message[3];
        Serial.print("Command: ");
    Serial.println(command, HEX);
    unsigned char value = message[6];
        Serial.print("Category: ");
    Serial.println(value, HEX);

    switch (category)
    {/*
        case 0x81: 
        {
        switch (command)
        {
            case 
        }
        break;
        }*/
        case 0x83:
        {
        switch (command)
        {
            case 0x81:
            {
            if (value == 0x01) {
                Serial.println("Falled detected");

                // Send LoRaWAN
                SendCommand("AT+CMSGHEX=\\"1234\\"");
                // Send Wifi
                sendPostRequest();
            } else {
                // Send LoRaWAN
                SendCommand("AT+CMSGHEX=\\"4321\\"");
                Serial.println("No fall detected");
            }
            break;
            }
        }
        break;
        }
    }
    }


    void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    //Serial1.begin(115200);

    // Serial for fall sensor
    Serial1.begin(115200, SERIAL_8N1, RX_Pin, TX_Pin);

    // Serial for lorawan module
    mySerial.begin(9600);


    WiFi.begin(ssid, password);

    // Wait for WiFi connection
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    while(!Serial || !Serial1);//When the serial port is opened, the program starts to execute.

    delay(1000);

    Serial.println("Connected to WiFi");

    x = 0;
    y = 0;
    state = 0;
    
    Serial.println("Ready");

    Serial1.write(turn_on, 10);

    Serial1.write(DevID_buff, 10);

    delay(10000);
    JoinNetwork();

    }




    void loop()
    {
    unsigned long currentMillis = millis();  // Get current time
    if (x > 100000)
    {
        x = 0;
        Serial1.write(query_fall, 10);
        //Serial.println("query fall");
    } 
    x++;
    
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;  // Save the last time the join network function is executed
        //JoinNetwork();
    }
    
    if (Serial1.available()) {
        unsigned char c = Serial1.read(); // Read byte from Serial1
        //Serial.print("Received from Serial1: ");
        //Serial.println(c, HEX);        // Print to Serial Monitor

        switch (state)
        {
        case 0:
            if (c == 0x53) {
            state = 1;
            }
            break;
        case 1:
            if (c == 0x59) {
            state = 2;
            Serial.println("started");
            } else {
            state = 0;
            }
            break;
        case 8:
            if (c == 0x54) {
            state = 9;
            }
            else {
            state = 0;
            Serial.println("failed");
            }
            break;
        case 9:
            if (c == 0x43) {
                Serial.println("message");
                parseMessage(receive);
            }
            else {
                Serial.println("failed");
            }
            state = 0;

            break;
        default:
            if (state >= 10) {
            state = 0;
            Serial.println("Overflow error");
            }
            else if (state > 1) {
            receive[state] = c;
            state++;
            }
            else {
            state = 0;
            }
    }
    }

    }
    """

    with open("./production_code/production_code.ino", "w") as file:
        file.write(content)
    # Call your function here with arg1 and arg2 as arguments



def update_board():
    boards = get_connected_arduino_ports()


update_board()


# Create the main application window
root = tk.Tk()
root.title("Function Executor")


update_button = tk.Button(root, text="Update Boards", command=update_board)
update_button.pack()

# Create input fields

label1 = tk.Label(root, text="wifi")
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="password")
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

label3 = tk.Label(root, text="devui")
label3.pack()
entry3 = tk.Entry(root)
entry3.pack()


label4 = tk.Label(root, text="app_key")
label4.pack()
entry4 = tk.Entry(root)
entry4.pack()

# Create a button to execute the function
execute_button = tk.Button(root, text="Execute Function", command=execute_function)
execute_button.pack()

# Start the main event loop
root.mainloop()