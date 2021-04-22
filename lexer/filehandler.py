import io


class FileHandler:
    def __init__(self, file_name: str, direct_input: bool = False):
        if not direct_input:
            self.file_name = file_name
            try:
                self.file = io.open(file_name, "r")
            except IOError:
                print("FILE NOT ACCESSIBLE")
        else:
            self.file_name = "STRING INPUT"
            self.file = io.StringIO(file_name)
        self.position = 0
        self.line = 1

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
