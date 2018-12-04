import argparse
import socket
import datetime
import json
from socketUtil import recv_msg, send_msg
from utils import GetPassword
from ClientOp import ClientOpGetEmail, ClientOpSendEmail, ClientOpStats

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--destination", action="store",
                    dest="address", default="localhost")
parser.add_argument("-p", "--port", action="store",
                    dest="port", type=int, default="12345")
args = vars(parser.parse_args())


def logError(error):
    print(error)
    fichier = open("Error.log", 'a')
    time = datetime.datetime.now().strftime("%b/%d/%Y::%I:%M%p\t")
    result = time + error + str("\n")
    fichier.write(result)
    fichier.close()


# initialisation des variables de connexion
destination = (args["address"], args["port"])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# open server communication
try:
    s.connect(destination)
except:
    print("La connexion n'a pu être établie au serveur de mail pour l'adresse: " +
          args["address"] + ":" + str(args["port"]))
    exit()

def MainLoop():
    while True:
        print("Menu principal")
        print("1. Envoi de courriels")
        print("2. Consultation de courriels")
        print("3. Statistiques")
        print("4. Quitter")

        try:
            value = int(input("Votre choix : "))
        except ValueError:
            value = 0

        if value is 1:
            ClientOpSendEmail(s)
        elif value is 2:
            ClientOpGetEmail(s)
        elif value is 3:
            ClientOpStats(s)
        elif value is 4:
            return
        else:
            print(
                "Erreur: Veuillez rentrer un chiffre correspondant à des choix proposés.")
            continue
    return

# Connection loop
while True:
    print("Menu de connexion")
    print("1. Se connecter")
    print("2. Creer un compte")

    toSendDict = {}

    try:
        value = int(input("Votre choix : "))
    except ValueError:
        value = 0

    if value is 1:
        toSendDict["msgType"] = "connection"
    elif value is 2:
        toSendDict["msgType"] = "newAccount"
    else:
        print("Erreur: Veuillez rentrer un chiffre correspondant à un des deux choix proposés.")
        continue

    username = input("Veuillez entrer votre nom d'utilisateur : ")
    mdp = GetPassword()
    toSendDict["username"] = username
    toSendDict["pwd"] = mdp

    # print("Sending: {0}", json.dumps(toSendDict))
    send_msg(s, json.dumps(toSendDict))
    received = recv_msg(s)
    # print("Received: {0}", received)

    receidAsDict = json.loads(received)
    if receidAsDict["msgType"] == "error":
        print("Erreur:", receidAsDict["errorType"])
        continue
    else:
        MainLoop()
        break
    # msg_received = recv_msg(s)

    # receivedDict = json.load(msg_received)

    # if server answered there was an error
    # if ErrorHandling(receivedDict):
    # s.close()
    # continue

s.close()



    

# program main loop
#while True:

# s.cl:ose()
