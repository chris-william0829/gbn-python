# packet.py

# Creates a packet from a sequence number and byte data
def make(seq_num, crc_num,data = b''):
    seq_bytes = seq_num.to_bytes(4, byteorder = 'little', signed = True)
    
    crc_bytes = crc_num.to_bytes(4,byteorder='little',signed=True)
    
    return seq_bytes + crc_bytes + data

# Creates an empty packet
def make_empty():
    return b''

# Extracts sequence number and data from a non-empty packet
def extract(packet):
    seq_num = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
    crc_num = int.from_bytes(packet[4:8], byteorder = 'little', signed = True)
    return seq_num, crc_num,packet[8:]
