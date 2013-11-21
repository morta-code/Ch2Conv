#!/usr/bin/python3

import lexer


class Parser:
    def __init__(self, lxr, rules, dest):
        self.lx = lxr
        self.dest_stream = dest
    
    def parse(self):
        token = self.lx.get_token()
        while token:
            print(token, file=self.dest_stream)
            token = self.lx.get_token()

