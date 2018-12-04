import getpass
from hashlib import sha256
import os.path

def HashText(plainText):
    hashedText = sha256(plainText.encode()).hexdigest()
    print("Texte hache : " + hashedText)
    return hashedText

def GetFileSize(fileName):
    size = os.path.getsize(fileName)
    print("Taille en octets : " + str(size))
    return size

def GetDirSize(dirPath):
    totalSize = 0
    for path, _, files in os.walk(dirPath):
        for f in files:
            filePath = os.path.join(path, f)
            totalSize += os.path.getsize(filePath)
    return totalSize

def GetPassword():
    return getpass.getpass("Password : ")

def CheckIfDirectoryExistsInCurrentDir(dirName):
    path = "./" + str(dirName)
    print("Checking if", path, "exists")
    return os.path.isdir(path)

def CheckIfFileExists(path):
    return os.path.exists(path)