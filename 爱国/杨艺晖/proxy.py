import socket
import threading
import re

def proxy(ser):
    conn,addr = ser.accept()
    data = conn.recv(1024)
    path_num = data.decode().find('\r\n')
    first_line = data.decode().split('\r\n',1)[0]# https 没处理好
    remain_line = data.decode().split('\r\n',1)[1]
    method,path_url,protocol = first_line.split()
    print(path_url)
    host = re.findall(r'(?<=://).*?(?=/)',path_url)[0]
    main_url = re.findall(r'.*?://',path_url)[0] + host
    path = path_url[len(main_url):]
    s_data = method + path + ' ' + protocol +" \n"+ remain_line+"\r\n"

    try:
        r_host = socket.gethostbyname(host)
        port = '80'
    except:
        if ':' in host:
            r_host,port = host.split(':')
        else:
            port = '80'
    s_s = socket.socket()
    print("""转发IP，port
--------------------------------------""")
    print(r_host,port)
    s_s.connect((r_host,int(port)))
    print("""转发请求数据：
-----------------------------""")
    print(s_data)
    s_s.send(s_data.encode())
    d = s_s.recv(1024)
    print("""转发响应数据:
-----------------------------""")
    print("d:{}".format(d))

    SER_ADDR = ('', 2080)#需要返回数据呀
    ser = socket.socket()
    ser.bind(SER_ADDR)
    ser.listen(5)
    ser.send(d)
    ser.close()

if __name__ == '__main__':

    while True:#需要一点错误处理
        try:
            t = threading.Thread(target=proxy(ser))
            t.start()
        except:
            pass
