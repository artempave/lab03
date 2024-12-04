import socket
from Library.LibServerConnection import LibServerConnection


class TranslateWord(LibServerConnection):
    def translate_word(self, text, start, end, result=None):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.send(sock, '01', 2)

            self.send(sock, text)
            self.send(sock, start)
            self.send(sock, end)

            flag_check_sql_request = self.recv(sock, 1)
            flag_int_sql_request = int(flag_check_sql_request)

            if flag_int_sql_request != 0:
                sock.close()
                print("Ошибка: Не удалось получить перевод")
                return self.ERROR_SYNTAX

            result.append(self.recv(sock))
            sock.close()

            return 0

        except Exception as e:
            print(f"{self.ERROR_TAG} Ошибка подключения: {e}")
            return self.ERROR_SERVER_CONNECTION
