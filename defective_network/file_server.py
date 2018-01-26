import socket
import threading
import os
import dsocket
import time

socket.socket = dsocket.deSocket

def RetrFile(name, sock):
    escolha = sock.recv(8).decode()
    if escolha[:2] == "DO":            ############ SEND FILE
        filename = sock.recv(19).decode()
        if os.path.isfile(filename):
            strd = ("EXISTE "+ str(os.path.getsize(filename)))
            sock.send(strd.encode())
            userResponse = sock.recv(19).decode()
            if userResponse[:2] == "OK":
                with open(filename,"rb") as f:
                    bytesToSend = f.read(19)
                    bytesToSend = bytesToSend + b'11111111111111111111'
                    sock.send(bytesToSend)
                    while (bytesToSend != b''):
                        bytesToSend = f.read(19)
                        if bytesToSend == b'':
                            confirmacao = "OK"
                            sent = sock.send(confirmacao.encode())
                            break
                        else:
                            if len(bytesToSend) < 19:
                                sock.send(bytesToSend)
                            else:
                                bytesToSend = bytesToSend + b'11111111111111111111'
                                sock.send(bytesToSend)
                    f.close()
        else:
            erro = "ERR"
            sock.send(erro.encode())
    if escolha[:2] == "UP":                                         ######## RECIEVE FILE
        print("seccao de upload do server")
        filename = sock.recv(19).decode()
        if os.path.isfile(filename):
            confirmacao = "OK"
            print("nome do ficheiro ",filename)
            sent = sock.send(confirmacao.encode())
            filesize = int(sock.recv(19).decode())
            sent = sock.send(confirmacao.encode())
            erros = 0
            f = open('upload_' + filename, 'wb')
            data = sock.recv(39)
            totalRecv = len(data)
            data = data[0:19]
            erros += 1
            f.write(data)
            while data[0:2] != "OK":
                data = sock.recv(39)
                if data == b'': break
                totalRecv += len(data)
                if len(data)<19:
                    f.write(data)
                    erros += 1
                else:
                    data = data[0:19]
                    erros += 1
                    f.write(data)
            print(" Download completo,  ocorreram {}".format(erros))
        else:
            print("o ficheiro nao existe")

def Main():
    host = '127.0.0.1'
    port = 5002

    s = socket.socket()
    s.bind((host,port))
    s.listen(5)

    print("O SERVIDOR INICIOU")
    while True:
        c, addr = s.accept()
        print(" client connected ip <" + str(addr)+">")
        t = threading.Thread(target=RetrFile, args=("retrThread" ,c))
        t.start()
    s.close()
if __name__ == '__main__':
    Main()