# -*- coding: utf-8 -*-
import socket, select
import traceback # para informação de excepções
from datetime import datetime

SOCKET_LIST = []    # lista de sockets abertos
RECV_BUFFER = 4096  # valor recomendado na doc. do python
PORT = 8088

def interpreta(data):    #simula uma interpretacao do sinal
    if(data == "0"):     #se o valor for 0 quer dizer que nao está humido logo tem que ligar a torneira, por isso envia se o sinal 1
        return "1"
    elif(data == "1"):  #vice versa
        return "0"

# função que trata dados do cliente
def faz_coisas(data, sock):

    addr = sock.getpeername()
    data = data.decode()
    print("Client %s\n\tMessage: '%s'" % (addr, data))
    valor = str(interpreta(data))
    #print("\nValue sent:",valor) #debug
    #print(str(datetime.now()))  #debug
    if (valor == "1"):
        humidade = "húmido"
    elif (valor == "0"):
        humidade = "seco"
    f = open('output.txt', 'a')
    f.write("\n<"+str(datetime.now())+"> <"+str(addr)+"><"+humidade+">") #escreve no ficheiro
    f.close()
    valor = valor.encode()
    sent = sock.send(valor)
    if sent == 0:
        raise RuntimeError("socket connection broken")


          
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))  # aceita ligações de qualquer lado
    server_socket.listen(100)
    server_socket.setblocking(0) # o socket deixa de ser blocking
    
    # Adicionamos o socket à lista de sockets a monitorizar
    SOCKET_LIST.append(server_socket)
    
    print("Server started on port %d" % (PORT,))

    timecount = 0
    while True:  # ciclo infinito

        # apagamos os sockets que "morreram" entretanto
        for sock in SOCKET_LIST:
            if sock.fileno() < 0:
                SOCKET_LIST.remove(sock)

        # agora, esperamos que haja dados em algum dos sockets que temos
        rsocks,_,_ = select.select(SOCKET_LIST,[],[], 5)

        if len(rsocks) == 0: # timeout
            timecount += 5
            print("Timeout on select() -> %d secs" % (timecount))
            if timecount % 60 == 0:  # passou um minuto
                timecount = 0
            continue
        
        for sock in rsocks:  # percorrer os sockets com nova informação
             
            if sock == server_socket: # há uma nova ligação
                newsock, addr = server_socket.accept()
                newsock.setblocking(0)
                SOCKET_LIST.append(newsock)
                
                print("New client - %s" % (addr,))
                 
            else: # há dados num socket ligado a um cliente
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data: 
                        faz_coisas(data, sock)
                        
                    else: # não há dados, o cliente fechou o socket
                        print("Client disconnected 1")
                        sock.close()
                        SOCKET_LIST.remove(sock)
                        
                except Exception as e: # excepção ao ler o socket, o cliente fechou ou morreu
                    print("Client disconnected")
                    print("Exception -> %s" % (e,))
                    print(traceback.format_exc())
                    
                    sock.close()
                    SOCKET_LIST.remove(sock)
                    
                    
