import argparse
import socket
import datetime

from socketUtil import recv_msg, send_msg
from ServerClient import ServerClient
from processing import ProcessClientLoop

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", action="store",
                    dest="port", type=int, default=12345)

args = vars(parser.parse_args())

def logError(error):
    print(error)
    fichier = open("Error.log", 'a')
    time = datetime.datetime.now().strftime("%b/%d/%Y::%I:%M%p\t")
    result = time + error + str("\n")
    fichier.write(result)
    fichier.close()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("localhost", args["port"]))
serversocket.listen(5)
print("Ecoute sur le port " + str(serversocket.getsockname()[1]))


while True:
    (s, address) = serversocket.accept()
    print("New client connected")

    client = ServerClient(s)

    ProcessClientLoop(client)

    s.close()
