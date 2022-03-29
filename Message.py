class Message:

    TERMINATOR = b'\n'
    SEPARATOR = b'\x7f'

    def __init__(self, typeName: str, args: [str]):
        self.typeName = typeName
        self.args = args

    def __repr__(self):
        s = f'Message({self.typeName}'

        for arg in self.args:
            s += f', {arg}'

        return s + ')'

    def to_bytes(self, encoding):
        arr = bytes(self.typeName, encoding)
        arr += Message.SEPARATOR

        first = True
        for arg in self.args:
            if first:
                first = False
            else:
                arr += Message.SEPARATOR

            arr += bytes(arg, encoding)

        arr += Message.TERMINATOR

        return arr
