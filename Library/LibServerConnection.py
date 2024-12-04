import socket
import logging

class LibServerConnection:
    SERVER_HOST = "povt-cluster.tstu.tver.ru"
    SERVER_PORT = 44040

    ERROR_SERVER_CONNECTION = -1
    ERROR_DB_CONNECTION = 1
    ERROR_DB_REQUEST = 2
    ERROR_SYNTAX = 3
    ERROR_CURRENCY = 4
    CORRECT_PERF = 0
    ERROR_TAG = "Error"

    @staticmethod
    def send(sock, data, size=None):
        try:
            if size is None:
                length_str = f"{len(data.encode()):08d}"
                sock.sendall(length_str.encode())
                sock.sendall(data.encode())
            else:
                sock.sendall(data.encode()[:size])
        except Exception as e:
            logging.error(f"Error sending data: {e}")
            raise

    @staticmethod
    def recv(sock, size=None):
        try:
            if size is None:
                size_str = LibServerConnection.recv(sock, 8)
                data_length = int(size_str)
                return LibServerConnection.recv(sock, data_length)
            else:
                data = sock.recv(size)
                return data.decode('UTF-8')
        except Exception as e:
            logging.error(f"Error receiving data: {e}")
            raise
