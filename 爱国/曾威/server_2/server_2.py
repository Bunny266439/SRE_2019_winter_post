#!/usr/bin/env python
# -*- coding:utf-8 -*-

from socket import *
import threading
import requests

def handle_url(url):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    }
    if url == '/':
        url_1 = "https://www.baidu.com"
        response = requests.get(url_1, headers=header)
        response.encoding = 'utf-8'
        http_response = response.text
        return http_response
    else:
        url_1 = "https://www.baidu.com"
        response = requests.get(url_1 + url, headers=header)
        response.encoding = 'utf-8'
        http_response = response.text
        return http_response


def parse_request(request_data):

    request_lines = request_data.split()
    if request_lines[0] == 'GET':
        return request_lines[1]


def handle_client(connection_socket):
    request_data = connection_socket.recv(1024).decode()
    print("request data:", request_data)
    url = parse_request(request_data)
    http_response = 'HTTP 200 OK/n/n' + handle_url(url)
    connection_socket.send(http_response.encode(encoding = 'UTF-8'))
    connection_socket.close()


if __name__ == '__main__':

    server_port = 9000
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(5)

    while True:
        connection_socket, addr = server_socket.accept()
        connection_socket.settimeout(1)
        print("[{}:{}]用户连接上了".format(addr[0], addr[1]))
        try:
            thread = threading.Thread(target=handle_client(connection_socket), args=(connection_socket))
            thread.start()
        except:
            connection_socket.close()