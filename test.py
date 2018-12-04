import smtplib
from email.mime.text import MIMEText

# remplissage des champs par l’utilisateur
mailfrom = input("Mail from : ")
rcptto = input("Rcpt to : ")
subject = input("Subject : ")
print("Data : ")
text = ""
temp = input()

while temp != ".":  
    text += temp + "\n"
    temp = input()

# creation d’un objet courriel avec MIMEText
msg = MIMEText(text)
msg["From"] = mailfrom
msg["To"] = rcptto
msg["Subject"] = subject
# envoi du courriel grace au protocole SMTP et au serveur de l’universite Laval
try:
    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
    smtpConnection.sendmail(mailfrom, rcptto, msg.as_string())
    smtpConnection.quit()
    print("Message envoye")
except:
    print("L’envoi n’a pas pu etre effectue. ")