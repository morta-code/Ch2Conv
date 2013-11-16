#!/usr/bin/python3

#import codecs
import re
import yaml
import sys
import text_reader
from argparse import ArgumentError


class Lexer:
    """ Lexikai elemző osztály.
    Paraméternek egy dictet (név: regkif), vagy egy listet ([(név, regkif)]) vár.
    put_text(str): puffer feltöltése str-vel
    get_token(end): Token generálása a pufferből.
        Az end jelzi, hogy a pufferen kívül van-e még betölthető szöveg. Ha None-nal tér vissza, akkor újra kell tölteni a puffert.
    """
    def __init__(self, rules, source):
        self.buffer = None
        self.r_list = list()
        self.limit = 10 #default max token hossz
        self.source = source
        self.s_type_l = True
        self.load_from_s = None
        self.end_of_source = False
        
        if type(source) == Lexer:
            self.s_type_l = True
            self.load_from_s = self._get_from_lx_
        elif type(source) == TextReader:
            self.s_type_l = False
            self.load_from_s = self._get_from_tr_
        else: raise ArgumentError("Not valid source type: {}. Lexer or TextReader expected".format(type(source)))
        
        if type(rules) == dict:
            for key,val in rules.items():
                build(key, val)
        elif type(rules) == list:
            for r in rules:
                key,val = r.popitem()
                build(key, val)
        else: raise ArgumentError("Not valid argument: {}. Expected dict of token definitions or list of list of name, def pairs".format(type(rules)))
        
        def build(k,v):
            """
            Szabályt felépítő eljárás
            """
            if k == '__maxlength__':
                self.limit = v
                return
            if type(v) == list:
                flags = 0
                if 'i' in v[1] : flags |= re.IGNORECASE
                if 'u' in v[1] : flags |= re.UNICODE
                if 'a' in v[1] : flags |= re.ASCII
                self.r_list.append( (re.compile(v[0], flags), k) )
            else:
                self.r_list.append( (re.compile(v), k) )
    
    
    def put_text(self, text):
        self.buffer += text
    
    def get_token(self, end_of_stream):
        #
        # String:
        #    Ha elég hosszú a puffer, akkor rákeresés a mintákra.
        #
        # Token:
        #    Ha üres, beolvasás.
        #    Ha van, és tovább kell adni, továbbadja.
        #    Ha van és elemezni kell, benyomja a tartalmát a pufferbe.
        #    
        if ( (len(self.buffer) < self.limit ) and not end_of_stream):
            return None
        for reg, name in self.r_list:
            mtch = reg.match(self.buffer)
            if mtch:
                self.buffer = self.buffer[len(mtch.group()):]
                return Token(name, mtch.group())
        else:
            if end_of_stream: return None
            raise BufferError("No match found. {}".format(self.buffer[0:10]))
    
    def is_end(self):
        return self.end_of_source
    
    def _get_from_tr_(self):
        self.buffer += self.source.read()
    
    def _get_from_lx_(self):
        pass



def main():
    y = yaml.load(open("tokens_list.yml"))
    lex = Lexer(y['tokens'])
    text = TextReader(open("George_Orwell_1984_tokenized_UTF-8_annotalt.txt"), 4096)
    
    for buffer in text:
        lex.put_text(buffer)
        tok = lex.get_token(text.is_end())
        while tok:
            print(tok.name, tok.value)
            tok = lex.get_token(text.is_end())
    print("Finished")
        


if __name__ == '__main__': main()