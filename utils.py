import getpass
from hashlib import sha256
from os.path import getsize, isdir, exists

def HashText(plainText):
    hashedText = sha256(plainText.encode()).hexdigest()
    print("Texte hache : " + hashedText)
    return hashedText


def GetFileSize(fileName):
    size = getsize(fileName)
    print("Taille en octets : " + str(size))
    return size

def GetPassword():
    return getpass.getpass("Password : ")

def CheckIfDirectoryExistsInCurrentDir(dirName):
    path = "./" + str(dirName)
    print("Checking if", path, "exists")
    return isdir(path)

def CheckIfFileExists(path):
    return exists(path)