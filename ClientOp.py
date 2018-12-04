import socket
import datetime
import json
from socketUtil import recv_msg, send_msg
from utils import GetPassword


# 1 - Get recipient, subject and content
# 2 - wrap it into json object and send it to the server
# 3 - Process the answer from the server
def ClientOpSendEmail(sock):
# 1 - Get recipient, subject and content
    recipient = input("Entrez l'adresse du destinataire: ")
    subject = input("Entrez le sujet du courriel: ")
    content = input("Entrez le contenu du courriel:\n")
    
# 2 - wrap it into json object and send it to the server
    # creation of the object to send
    toSend = {"msgType": "sendEmail", "recipient": recipient, "subject": subject, "content": content}
    
    # serialization as json
    toSendAsJson = json.dumps(toSend)

    # print("Sending: " + toSendAsJson)
    try:
        send_msg(sock, toSendAsJson)
        received = recv_msg(sock)
    except:
        print("Erreur: le serveur semble s'être arreté, le client doit donc se fermer.")
    # print("Received: {0}", received)

# 3 - Process the answer from the server
    # deserialization of the received answer from the server
    receivedAsDict = json.loads(received)

    if receivedAsDict["msgType"] == "error":
        print("Erreur: ", receivedAsDict["errorType"])
        return
    print("Succès: Le message a été avec succès.")
    return

# 1 - Send the getEmail request to the server
# 2 - Get the server's answer and write it
# 3 - Get the user's choice
# 4 - Send the server the number user has chosen
# 5 - Get the answer from the server and write it
def ClientOpGetEmail(sock):
# 1 - Send the getEmail request to the server
    toSend = {"msgType": "getEmail"}

    # serialization as json
    toSendAsJson = json.dumps(toSend)

# 2 - Get the server's answer and write it
    # print("Sending: " + toSendAsJson)
    try:
        send_msg(sock, toSendAsJson)
        received = recv_msg(sock)
    except:
        print("Erreur: le serveur semble s'être arreté, le client doit donc se fermer.")
    # print("Received: {0}", received)

    receivedAsDict = json.loads(received)
    
    if receivedAsDict["msgType"] == "error":
        print("Erreur:", receivedAsDict["msgType"])
        return
    
    if 'mailList' not in receivedAsDict:
        print("Erreur: le serveur ne possède pas de liste d'email")
        return
    
    mailList = receivedAsDict["mailList"]
    
    if len(mailList) is 0:
        print("Info: votre liste de courriels accessibles est actuellement vide")
        return
    
    print("La liste de courriels accessibles a une longueur de: " + str(len(mailList)) + " courriels.")
    incr = 1
    for subject in mailList:
        print(str(incr) + ".\t" + subject)
        incr += 1
    
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
    toSend = {"msgType": "getEmail", "chosenEmailIndex": value - 1}
    
    toSendAsJson = json.dumps(toSend)

    try:
        send_msg(sock, toSendAsJson)
        received = recv_msg(sock)
    except:
        print("Erreur: le serveur semble s'être arreté, le client doit donc se fermer.")
    # print("Sending: " + toSendAsJson)
    # print("Received: {0}", received)

# 5 - Get the answer from the server and write it
    receivedAsDict = json.loads(received)

    if receivedAsDict["msgType"] == "error":
        print("Erreur:", receivedAsDict["msgType"])
        return
    print() 
    print("Destinataire:\t", receivedAsDict["recipient"])
    print("Envoyeur:\t", receivedAsDict["sender"])
    print("Date:\t", receivedAsDict["date"])
    print()
    print()
    print("Sujet:", receivedAsDict["subject"])
    print()
    print()
    print(receivedAsDict["content"])
    print()
    print()

    input("Appuyer sur entré pour continuer...")

    return

def ClientOpStats(sock):
    toSend = {"msgType": "stats"}

    # serialization as json
    toSendAsJson = json.dumps(toSend)

    try:
        send_msg(sock, toSendAsJson)
        received = recv_msg(sock)
    except:
        print("Erreur: le serveur semble s'être arreté, le client doit donc se fermer.")

    receivedAsDict = json.loads(received)
    if (receivedAsDict["msgType"] == "error"):
        print("Error:", receivedAsDict["errorType"])
        input("Appuyer sur entré pour continuer...")
        return

    subjectList = receivedAsDict["subjectList"]
    dirSize = receivedAsDict["dirSize"]

    print()
    print("Nombre total d'email: " + str(len(subjectList)) + ".")
    print("Taille totale de votre dossier utilisateur sur le serveur: " + str(dirSize / 1000) + "kb.")
    if len(subjectList) == 0:
        return
    print()
    print("Liste des sujets de vos courriels:")
    print('\n'.join(subjectList))
    print()
    input("Appuyer sur entré pour continuer...")

