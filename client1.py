import socket, time
from random import randint

def start_water():
    print("Abrir torneira")

def stop_water():
    print("Fechar torneira")

def humidade():
    valor = randint(0,1)
    return valor

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8088))
while True:

    valor = humidade()
    valor = str(valor)
    print("\n[client]Value sent",valor)
    sent = clientsocket.send(valor.encode())
    if sent == 0:
        raise RuntimeError("socket connection broken")
    result = clientsocket.recv(128)
    result = result.decode()
    print(type(result))
    print("[client]Value recieved)\n" ,result)
    time.sleep(5)
    print("\nAcção:")
    if(result == "1"):
        start_water()
    elif(result == "0"):
        stop_water()


