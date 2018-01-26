import os
import socket
import dsocket
import time

socket.socket = dsocket.deSocket

def getSize(filename):
    st = os.stat(filename)
    return st.st_size


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 5002))
if input("download ou upload? (d/u)") == "d":
    downloadsignal = "DOWLOAD"
    sent = clientsocket.send(downloadsignal.encode())
    if sent == 0:
        raise RuntimeError("socket connection broken")
    filename = input("Nome do ficheiro?")
    if filename != 'e':
        sent = clientsocket.send(filename.encode())
        if sent == 0:
            raise RuntimeError("socket connection broken")
        data = clientsocket.recv(19).decode()
        if data[:6] == 'EXISTE':
            filesize = int(data[6:])
            message = input("O ficheiro existe, quer fazer o download? (y/n)")
            if message == "y":
                confirmacao = "OK"
                sent = clientsocket.send(confirmacao.encode())
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                erros = 0
                f = open('download_'+filename, 'wb')
                data = clientsocket.recv(39)
                totalRecv = len(data)
                data = data[0:19]
                erros += 1
                f.write(data)
                while data[0:2] != b"OK":
                    data = clientsocket.recv(39)

                    if data == b'OK': break
                    totalRecv += len(data)
                    if len(data) < 19:
                        f.write(data)
                        erros += 1
                    else:
                        data = data[0:19]
                        erros += 1
                        f.write(data)
                print(" Download completo,  ocorreram {}".format(erros))
        else:
            print("o ficheiro nao existe")
else:               ######################################################  UPLOAD
    downloadsignal = "UPLOAD "
    sent = clientsocket.send(downloadsignal.encode())
    if sent == 0:
        raise RuntimeError("socket connection broken")
    filename = input("Nome do ficheiro?")
    if filename != 'e':
        if os.path.isfile(filename):
            print("O ficheiro existe")
            sent = clientsocket.send(filename.encode())     #MANDA NOME FICHEIRO
            if sent == 0:
                raise RuntimeError("socket connection broken")
            strd = (str(os.path.getsize(filename)))
            userResponse = clientsocket.recv(19).decode()  #RECEBE CONFIRMACAO
            if userResponse[:2] == "OK":
                clientsocket.send(strd.encode())    #MANDA TAMANHO DO FICHEIRO
                userResponse = clientsocket.recv(19).decode()  #RECEBE CONFIRMACAO
                if userResponse[:2] == "OK":        #MANDA FICHEIRO
                    with open(filename, "rb") as f:
                        bytesToSend = f.read(19)
                        bytesToSend = bytesToSend + b'11111111111111111111'
                        clientsocket.send(bytesToSend)
                        while(bytesToSend !=b''):
                            bytesToSend = f.read(19)
                            if bytesToSend == b'':
                                break
                            else:
                                if len(bytesToSend)<19:
                                    clientsocket.send(bytesToSend)
                                else:
                                    bytesToSend = bytesToSend + b'11111111111111111111'
                                    clientsocket.send(bytesToSend)

                        f.close()
        else:
            print("o ficheiro nao existe")
            erro = "ERR"
            clientsocket.send(erro.encode())
clientsocket.close()