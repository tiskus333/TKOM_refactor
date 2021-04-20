class Token:
    def __init__(self, type, value, position) -> None:
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return f'Token({self.type}, {self.value}, {self.position})'
