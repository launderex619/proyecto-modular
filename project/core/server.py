from comms import tcp_comms as tcp
import time


def start():
    # Create TCP socket to use for sending (and receiving)
    sock = tcp.TcpComms(tcpIP="127.0.0.1", portTX=5000,
                        portRX=5001, suppressWarnings=True)

    i = 0

    while True:
        # Send this string to other application
        if sock.connectedSender:
            sock.SendData('Sent from Python: ' + str(i))
            i += 1
        if sock.connectedListener:
            data = sock.ReadReceivedData()  # read data
            if data != None:  # if NEW data has been received since last ReadReceivedData function call
                print(data)  # print new received data

        time.sleep(5)
