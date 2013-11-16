import lexer
import text_reader

class Parser:
    def __init__(self, lexer, dest):
        self.lx = lexer
        self.dest_stream = dest
    
    def parse():
        token = self.lx.get_token()
        while token:
            print(token)
            token = self.lx.get_token()

