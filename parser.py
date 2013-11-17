#!/usr/bin/python3

import lexer
import text_reader

class Parser:
    def __init__(self, lexer, rules, dest=sys.stdout):
        self.lx = lexer
        self.dest_stream = dest
    
    def parse():
        token = self.lx.get_token()
        while token:
            print(token, file=self.dest_stream)
            token = self.lx.get_token()

