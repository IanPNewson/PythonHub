class Message:

    def __init__(self, typeName: str, args: [str]):
        self.typeName = typeName
        self.args = args

    def __repr__(self):
        s = f'Message({self.typeName}'

        for arg in self.args:
            s += f', {arg}'

        return s + ')'
