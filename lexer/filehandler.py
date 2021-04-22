import io


class FileHandler:
    def __init__(self, file_name: str, direct_input: bool = False):
        self.direct_input = direct_input
        if not direct_input:
            self.file_name = file_name
            try:
                self.file = open(file_name, "r")
            except IOError:
                print("FILE NOT ACCESSIBLE")
        else:
            self.file_name = "STRING INPUT"
            self.file = io.StringIO(file_name)
        self.position = 0
        self.line = 1

    def __del__(self):
        if not self.direct_input:
            self.file.close()

    def nextChar(self):
        self.curr_char = self.file.read(1)
        if self.curr_char != '':
            self.position += 1
        if self.curr_char == '\n':
            self.line += 1
            self.position = 0
        return self.curr_char

    def currChar(self):
        return self.curr_char
