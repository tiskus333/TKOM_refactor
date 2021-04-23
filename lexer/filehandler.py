import io


class FileHandler:
    def __init__(self, file_name: str, direct_input: bool = False):
        self.__direct_input = direct_input
        if not self.__direct_input:
            self.__file_name = file_name
            try:
                self.__file = open(self.__file_name, "r")
            except IOError:
                raise IOError

        else:
            self.__file_name = "STRING INPUT"
            self.__file = io.StringIO(file_name)
        self.__column = 0
        self.__line = 1

    def __del__(self):
        if not self.__direct_input:
            try:
                self.__file.close()
            except:
                pass

    def nextChar(self):
        self.__curr_char = self.__file.read(1)
        if self.__curr_char != '':
            self.__column += 1
        if self.__curr_char == '\n':
            self.__line += 1
            self.__column = 0
        return self.__curr_char

    def currChar(self):
        return self.__curr_char

    def getPosition(self):
        return (self.__line, self.__column)

    def getFileName(self):
        return self.__file_name
