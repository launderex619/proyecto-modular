import socket
import threading


class TcpComms():
    def __init__(self, tcpIP, portTX, portRX, suppressWarnings=True):
        """
        Constructor
        :param tcpIP: Must be string e.g. "127.0.0.1"
        :param portTX: integer number e.g. 5000. Port to transmit from i.e From Python to other application
        :param portRX: integer number e.g. 5001. Port to receive on i.e. From other application to Python
        :param enableRX: When False you may only send from Python and not receive. If set to True a thread is created to enable receiving of data
        :param suppressWarnings: Stop printing warnings if not connected to other application
        """

        self.tcpIP = tcpIP
        self.tcpSendPort = portTX
        self.tcpRcvPort = portRX
        self.suppressWarnings = suppressWarnings  # when true warnings are suppressed
        self.isDataReceived = False
        self.dataRX = None
        self.connectedListener = False
        self.connectedSender = False
        self.client = None
        self.clientAddress = None

        # Connect via TCP
        # internet protocol, tcp (SOCK_STREAM) socket
        self.tcpSockListener = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSockSender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state waiting for late packets to arrive.
        self.tcpSockListener.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpSockSender.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # await for client
        self.connectListener()
        self.connectSender()
        # Create Receiving thread if required
        # if enableRX:
        self.rxThread = threading.Thread(
            target=self.ReadTcpThreadFunc, daemon=True)
        self.rxThread.start()

    def __del__(self):
        self.CloseSocket()

    def connectSender(self):
        # Connect to client
        while not self.connectedSender:
            print("connecting sender...")
            try:
                self.tcpSockSender.connect((self.tcpIP, self.tcpSendPort))
                self.connectedSender = True
            except Exception as e:
                pass  # Do nothing, just try again

    def connectListener(self):
        # Connect to client
        while not self.connectedListener:
            print("connecting listener...")
            try:
                self.tcpSockListener.bind((self.tcpIP, self.tcpRcvPort))
                self.tcpSockListener.listen()
                self.client, self.clientAddress = self.tcpSockListener.accept()
                self.connectedListener = True
            except Exception as e:
                pass  # Do nothing, just try again

    def CloseSocket(self):
        # Function to close socket
        self.tcpSockListener.close()

    def SendData(self, strToSend):
        # Use this function to send string to C#
        # self.tcpSockListener.sendto(bytes(strToSend, 'utf-8'),
        #                     (self.tcpIP, self.tcpSendPort))
        if self.connectedSender:
            self.tcpSockSender.send(bytes(strToSend, 'utf-8'))

    def ReceiveData(self):
        """
        Should not be called by user
        Function BLOCKS until data is returned from C#. It then attempts to convert it to string and returns on successful conversion.
        An warning/error is raised if:
            - Warning: Not connected to C# application yet. Warning can be suppressed by setting suppressWarning=True in constructor
            - Error: If data receiving procedure or conversion to string goes wrong
            - Error: If user attempts to use this without enabling RX
        :return: returns None on failure or the received string on success
        """

        data = None
        try:
            if self.connectedListener:
                data, _ = self.client.recvfrom(1024)
                data = data.decode('utf-8')
            else:
                pass
        except WindowsError as e:
            if e.winerror == 10054:  # An error occurs if you try to receive before connecting to other application
                if not self.suppressWarnings:
                    print("Are You connected to the other application? Connect to it!")
                else:
                    pass
            else:
                raise ValueError(
                    "Unexpected Error. Are you sure that the received data can be converted to a string")

        return data

    def ReadTcpThreadFunc(self):  # Should be called from thread
        """
        This function should be called from a thread [Done automatically via constructor]
                (import threading -> e.g. tcpReceiveThread = threading.Thread(target=self.ReadTcpNonBlocking, daemon=True))
        This function keeps looping through the BLOCKING ReceiveData function and sets self.dataRX when data is received and sets received flag
        This function runs in the background and updates class variables to read data later
        """
        while True:
            if (self.connectedListener):
                self.isDataReceived = False  # Initially nothing received
                # Blocks (in thread) until data is returned (OR MAYBE UNTIL SOME TIMEOUT AS WELL)
                data = self.ReceiveData()
                self.dataRX = data  # Populate AFTER new data is received
                self.isDataReceived = True
                # When it reaches here, data received is available

                # Stuff to do with received data:
                print(data)
            else:
                self.connectListener()

    def ReadReceivedData(self):
        """
        This is the function that should be used to read received data
        Checks if data has been received SINCE LAST CALL, if so it returns the received string and sets flag to False (to avoid re-reading received data)
        data is None if nothing has been received
        :return:
        """
        if (self.connectedListener):
            data = None

            if self.isDataReceived:  # if data has been received
                self.isDataReceived = False
                data = self.dataRX
                self.dataRX = None  # Empty receive buffer
            return data
        else:
            self.connectListener()
            return None
