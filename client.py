import argparse
import socket
import datetime
import json
from socketUtil import recv_msg, send_msg
from utils import GetPassword

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
# todo connection error

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

    print("Sending: {0}", json.dumps(toSendDict))
    send_msg(s, json.dumps(toSendDict))
    received = recv_msg(s)
    print("Received: {0}", received)

    receidAsDict = json.loads(received)
    if receidAsDict["msgType"] == "error":
        print("Erreur:", receidAsDict["errorType"])
        continue

    break
    # msg_received = recv_msg(s)

    # receivedDict = json.load(msg_received)

    # if server answered there was an error
    # if ErrorHandling(receivedDict):
    # s.close()
    # continue

s.close()


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
            ClientOpSendEmail()
        elif value is 2:
            toSendDict["msgType"] = "getEmail"
        elif value is 3:
            toSendDict["msgType"] = "stats"
        elif value is 4:
            return
        else:
            print(
                "Erreur: Veuillez rentrer un chiffre correspondant à un des deux choix proposés.")
            continue

        print("Sending: {0}", json.dumps(toSendDict))
        send_msg(s, json.dumps(toSendDict))
        received = recv_msg(s)
        print("Received: {0}", received)

    return

# 1 - Get recipient, subject and content
# 2 - wrap it into json object and send it to the server
# 3 - Process the answer from the server
def ClientOpSendEmail():
# 1 - Get recipient, subject and content
    recipient = input("Entrez l'adresse du destinataire: ")
    subject = input("Entrez le sujet du courriel: ")
    content = input("Entrez le contenu du courriel:\n")
    
# 2 - wrap it into json object and send it to the server
    # creation of the object to send
    toSend = {"msgType": "sendEmail", "recipient": recipient, "subject": subject, "content": content}
    
    # serialization as json
    toSendAsJson = json.dumps(toSend)

    print("Sending: " + toSendAsJson)
    send_msg(s, toSendAsJson)
    received = recv_msg(s)
    print("Received: {0}", received)

# 3 - Process the answer from the server
    # deserialization of the received answer from the server
    receivedAsDict = json.loads(received)

    if receidAsDict["msgType"] == "error":
        print("Erreur: ", receidAsDict["msgType"])
        return
    print("Succès: Le message a été avec succès.")
    return

# 1 - Send the getEmail request to the server
# 2 - Get the server's answer and write it
# 3 - Get the user's choice
# 4 - Send the server the number user has chosen
# 5 - Get the answer from the server and write it
def ClientOpGetEmail():
# 1 - Send the getEmail request to the server
    toSend = {"msgType": "getEmail"}

    # serialization as json
    toSendAsJson = json.dumps(toSend)

# 2 - Get the server's answer and write it
    print("Sending: " + toSendAsJson)
    send_msg(s, toSendAsJson)
    received = recv_msg(s)
    print("Received: {0}", received)

    receidAsDict = json.loads(received)
    
    if receidAsDict["msgType"] == "error":
        print("Erreur:", receidAsDict["msgType"])
        return
    
    if 'mailList' not in receidAsDict:
        print("Erreur: le serveur ne possède pas de liste d'email")
        return
    
    mailList = receidAsDict["mailList"]
    
    if len(mailList) is 0:
        print("Info: votre liste de courriels accessebles est actuellement vide")
        return
    
    print("La liste de courriels accessibles a une longueur de: " + str(len(mailList)) + " courriels.")
    incr = 1
    for subject in mailList:
        print(str(incr) + ".\t" + subject)
    
# 3 - Get the user's choice
    value = 0
    while True:
        try:
            value = int(input("Entrez le numéro du courriel que vous souhaitez consulter: "))
        except ValueError:
            value = 0

        if value <= 0 or value > len(mailList):
            print("Erreur: ce que vous avez entré n'est pas un numéro valide")
            continue
        break        

# 4 - Send the server the number user has chosen
    toSend = {"msgType": "getEmail", "chosenEmailIndex": value}
    
    toSendAsJson = json.dumps(toSend)

    print("Sending: " + toSendAsJson)
    send_msg(s, toSendAsJson)
    received = recv_msg(s)
    print("Received: {0}", received)

# 5 - Get the answer from the server and write it
    receidAsDict = json.loads(received)

    if receidAsDict["msgType"] == "error":
        print("Erreur:", receidAsDict["msgType"])
        return
    
    print("Destinataire:", receidAsDict["recipient"])
    print("Envoyeur:", receidAsDict["sender"])
    print("Sujet:", receidAsDict["subject"])
    print("Date:", receidAsDict["date"])
    print("Contenu:\n", receidAsDict["content"])
    return

    

# program main loop
#while True:

# s.cl:ose()
