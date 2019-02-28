import socket
import struct
import select
import threading


def handle_socks5(sock):

    sock.recv(256)
    sock.send(b"\x05\x00")
    socks5_data = sock.recv(4)
    ATYP = socks5_data[3]
    if ATYP == 1:
        addr_ipv4 = sock.recv(4)
        remote_addr = socket.inet_ntop(socket.AF_INET,addr_ipv4)
    elif ATYP == 3:
        addr_name_len = int.from_bytes(sock.recv(1), byteorder='big')
        remote_addr = sock.recv(addr_name_len)
    elif ATYP == 4:
        addr_ipv6 = sock.recv(16)
        remote_addr = socket.inet_ntop(socket.AF_INET6,addr_ipv6)
    else:
        return
    remote_addr_port = struct.unpack('>H', sock.recv(2))

    reply = b"\x05\x00\x00\x01"
    reply += socket.inet_aton('0.0.0.0')
    reply += struct.pack(">H", 8000)
    sock.send(reply)

    remote_socket = socket.create_connection((remote_addr, remote_addr_port[0]))

    handle_tcp(sock, remote_socket)



def handle_tcp(sock,remote):

    fdset = [sock, remote]
    try:
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                data = sock.recv(4096)
                if len(data) == 0:
                    break
                print(data)
                remote.send(data)
            if remote in r:
                data = remote.recv(4096)
                if len(data) == 0:
                    break
                print(data)
                sock.send(data)
    except:
        sock.close()
        remote.close()
    finally:
        sock.close()
        remote.close()


if __name__ == '__main__':
    server_port = 8000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', server_port))
    server_socket.listen(5)

    while True:
        connection_socket,addr = server_socket.accept()
        connection_socket.settimeout(1)
        try:
            thread = threading.Thread(target=handle_socks5(connection_socket), args=(connection_socket))
            thread.start()
        except:
            connection_socket.close()