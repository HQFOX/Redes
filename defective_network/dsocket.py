import random
import socket

class deSocket(socket.socket):

    @staticmethod
    def _nextbyte():
        random.seed()
        return random.randrange(20,40)

    def send(self, data):
        random.seed()
        err = deSocket._nextbyte()
        print('err = %d' % (err))
        cnt = 1
        newdata = []

        for b in data:
            if cnt % err == 0:
                newdata.append(random.randrange(33,125))
            else:
                newdata.append(b)
                
            cnt+=1

        return super().send(bytes(newdata))
