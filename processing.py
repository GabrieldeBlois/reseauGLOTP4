import json
import re
import os
import datetime
import socket
from socketUtil import recv_msg, send_msg
from utils import HashText, GetFileSize, CheckIfDirectoryExistsInCurrentDir, CheckIfFileExists

# the inside loop for each client
# 1 - get the next msg from the client
# 2 - Check if the client is already authentified
# 3 - Send the message resulting from the processing
def ProcessClientLoop(client):
    while True:
# 1 - get the next msg from the client
        try:
            msgReceivedAsJson = recv_msg(client.sock)
        except:
            print("User disconnected")
            return
        msgReceivedAsDict = json.loads(msgReceivedAsJson)

        msgToSend = {}

# 2 - Check if the client is already authentified
        if client.state is 0:
            msgToSend = ProcessNotAuthentifiedClient(client, msgReceivedAsDict)
        elif client.state is 1:
            msgToSend = ProcessAuthentifiedClient(client, msgReceivedAsDict)
        
# 3 - Send the message resulting from the processing
        # try sending the message to the client
        try:
            send_msg(client.sock, json.dumps(msgToSend))
        except:
            print("Error: client disconnected")
            return

def ProcessNotAuthentifiedClient(client, msg):
    if msg["msgType"] == "connection":
        print("New operation requested: connection")
        return ProcessConnection(client, msg)
    elif msg["msgType"] == "newAccount":
        print("New operation requested: newAccount")
        return ProcessNewAccountRequest(client, msg)
    # not recognized msgType
    return {"msgType": "error", "errorType": "Vous devez vous connecter avant de pouvoir effectuer des opérations autres que la création de compte ou la connexion."}

def ProcessAuthentifiedClient(client, msg):
    if msg["msgType"] == "sendEmail":
        print("New operation requested: sendEmail")
        return ProcessSendEmail(client, msg)
    elif msg["msgType"] == "getEmail":
        print("New operation requested: getEmail")
        return
    elif msg["msgType"] == "stats":
        print("New operation requested: stats")
        return
    # not recognized msgType
    return {"msgType": "error", "errorType": "L'operation demandée n'est pas disponible"}

# 1 - check if there are problems with the received username and password, 
# 2 - then tranlate pwd into hashed string, 
# 3 - fill the client and the outMsg object that are mutable
def ProcessAuthOrConnectionCheckUsernamePassword(client, msg, outMsg):
    # check if the is no username or no password in the received object
    if 'username' not in msg.keys() or 'pwd' not in msg.keys():
        outMsg["msgType"] = "error"
        outMsg["errorType"] = "Vous devez impérativement envoyer un nom d'utilisateur et un mot de passe"
        return False
    
    username = msg["username"]
    password = msg["pwd"]

    # check if the username is empty
    if username == "":
        outMsg["msgType"] = "error"
        outMsg["errorType"] = "Votre nom d'utilisateur doit posséder au moins un caractère."
        return False

    client.username = username
    client.pwd = HashText(password)
    return True

# 1 - Check if the username and pwd has been sent
# 2 - Check if a user exists for a given username
# 3 - Check if the two hashed pwd match
# 4 - Change the client state to "connected" and answer "ok" to the client
def ProcessConnection(client, msg):
    outMsg = {"msgType": "ok"}
    if not ProcessAuthOrConnectionCheckUsernamePassword(client, msg, outMsg):
        return outMsg

    if not CheckIfDirectoryExistsInCurrentDir(client.username):
        return {"msgType": "error", "errorType": "Ce nom d'utilisateur n'existe pas"}
    
    client.userPath = "./" + str(client.username) + "/"

    configFile = open(client.userPath + "config.txt", 'r')
    hashedPwd = configFile.read()

    if hashedPwd != client.pwd:
        return {"msgType": "error", "errorType": "Le mot de passe ne correspond pas"}

    print("Client connected successfuly")
    # the username and the password are right
    client.state = 1
    return {"msgType": "ok"}

# 1 - Check if the username and pwd has been sent
# 2 - Check if a user exists for a given username
# 3 - Check if the password is well formated
# 4 - Create folder and config.txt with hashed pwd
# 5 - Change the client state to "connected" and answer "ok" to the client
def ProcessNewAccountRequest(client, msg):
    print("New account creation requested for username = {0} with pwd = {1}", msg["username"], msg["pwd"])
    outMsg = {"msgType": "ok"}
    if not ProcessAuthOrConnectionCheckUsernamePassword(client, msg, outMsg):
        return outMsg
    if CheckIfDirectoryExistsInCurrentDir(client.username):
        return {"msgType": "error", "errorType": "Ce nom d'utilisateur est déja pris"}
    
    print("check pwd format")
    # j'ai utilisé https://regex101.com pour créer cette regex
    p = re.compile(r"^(?=\D*\d)(?=.*[a-zA-Z])\S{6,12}$")
    if p.match(msg["pwd"]) is None:
        return {"msgType": "error", "errorType": "Le mot de passe ne correspond pas à la charte: le mot de passe doit être compris en 6 et 12 caractères dont au moins un chiffre et une lettre"}

    print("creation of the new user folder")
    os.makedirs(client.username)
    client.userPath = "./" + str(client.username) + "/"

    print("Creation of the new user config file with hashed pwd in it")
    file = open(client.userPath + "config.txt", 'w+')
    file.write(client.pwd)
    file.close()

    print("Creation of the new user secceeded")
    # the username and the password are right
    client.state = 1
    return {"msgType": "ok"}

# 1 - Check if the recipient exists
# 2 - Open the email file or create it if needed
# 3 - Get all already existing emails
# 4 - Feed the email list with the new mail
# 5 - write it to the email json file
# 6 - close the email file
def ProcessSendLocalEmail(client, msg, recipientUserName):
    path = "./"
# 1 - Check if the recipient exists
    if not CheckIfDirectoryExistsInCurrentDir(recipientUserName):
        if not CheckIfDirectoryExistsInCurrentDir("./DESTERREUR"):
            os.makedirs("./DESTERREUR")
        path += "DESTERREUR/"
    else:
        path += recipientUserName + "/"
    
# 2 - Open the email file or create it if needed
    emailFile = open(path + "emaillist.json", 'w+')
    
    # read
    rawContent = emailFile.read()
    
# 3 - Get all already existing emails
    emaillist = []
    if rawContent != "":
        emaillist = json.loads(rawContent)
    
# 4 - Feed the email list with the new mail
    emaillist.append(msg)

# 5 - write it to the email json file
    rawContent = json.dumps(emaillist)
    emailFile.write(rawContent)
# 6 - close the email file
    emailFile.close()
    return {"msgType": "ok"}


def ProcessSendExternalEmail(client, msg, recipientEmailAddress):
    return {"msgType": "ok"}


# 1 - Error handling on the received message
# 2 - Check if the address is well formated
# 3 - Add date and sender information to the email packet
# 4 - Check if it s a local address or an external one
def ProcessSendEmail(client, msg):
# 1 - Error handling on the received message
    if "recipient" not in msg.keys():
        return {"msgType": "error", "errorType": "Le destinataire est un champ obligatoire."}
    if "subject" not in msg.keys():
        return {"msgType": "error", "errorType": "Le sujet est un champ obligatoire."}
    if "content" not in msg.keys():
        return {"msgType": "error", "errorType": "Le contenu est un champ obligatoire."}

# 2 - Check if the address is well formated
    # this is the official RFC 5322 Regex. Taken from https://emailregex.com/
    p = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    recipient = str(msg["recipient"])

    match = p.match(recipient)
    if match is None:
        return {"msgType": "error", "errorType": "Adresse courriel non valide: " + recipient}

# 3 - Add date and sender information to the email packet
    msg["sender"] = client.username + "@reseauglo.ca"
    msg["date"] = datetime.datetime.now().strftime("%b/%d/%Y::%I:%M%p")

# 4 - Check if it s a local address or an external one
    splittedRecipient = recipient.split('@')
    username = splittedRecipient[0]
    host = splittedRecipient[1]

    if host == "reseauglo.ca":
        return ProcessSendLocalEmail(client, msg, username)
    else:
        return ProcessSendExternalEmail(client, msg, recipient)