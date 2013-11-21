#!/usr/bin/python3

import re
import text_reader

####################################################################################################


class Action:
    """ Action osztály a találatok kezelésére
    Action(opt, name, modulename)
        opt: True, False, külső_metórdusnév
        name: Generálandó token neve
        modulename: Féjl/modul neve, ahonnan a külső függvényt hívjuk
    self.action(match_str, row, column) : tuple
        A talált lexémára létrehozza a megfelelő tokent
    """
    def __init__(self, opt=None, name=None, modulename=None):
        self.token_name = name
        self.action = None
        if type(opt) == bool:
            if opt:
                self.action = self._action_with_v
            else:
                self.action = self._action_withtout_v
        elif type(opt) == str:
            self.action = self._action_with_external_call
            #runfile(modulename) # TODO importlib.import_module
            self.external_call = locals()[opt]
        else:
            self.action = self._action_for_ignore
        
    
    def _action_with_v(self, match_str, row, column):
        return self.token_name, match_str, row, column
    
    def _action_withtout_v(self, match_str, row, column):
        return self.token_name, None, row, column

    def _action_with_external_call(self, match_str, row, column):
        match_str = self.external_call(match_str) #getattr(self.mod, self.external_call)(match_str)
        return self.token_name, match_str, row, column
    
    def _action_for_ignore(self, match_str, row, column):
        return None

####################################################################################################


class Lexer:
    """ Lexikai elemző osztály.
    Paraméternek egy dictet (név: regkif), vagy egy listet ([(név, regkif)]) vár.
    put_text(str): puffer feltöltése str-vel
    get_token(end): Token generálása a pufferből.
        Az end jelzi, hogy a pufferen kívül van-e még betölthető szöveg. Ha None-nal tér vissza, akkor újra kell tölteni a puffert.
    """
    def __init__(self, name, rules, source):
        self.name = name
        self.source = source
        self.buffer = ""
        self.get_token = None
        self.rules = []     # TODO
        self.row = 0
        self.column = 0
        
        def init_as_text():
            self.get_token = self._get_from_tr_
            self.max_lex_len = 25 # default érték
            for r in rules:
                rnam, rval = r.popitem()
                if rnam == '__maxlength__':
                    self.max_lex_len = rval
                elif rnam == '__ignore__':
                    self.rules.append((re.compile(rval[0]), Action()))
                else:
                    self.rules.append((re.compile(rval[0]), Action(rval[1], rnam)))

        def init_as_lex():
            self.get_token = self._get_from_lx_
            self.tok = None
            self.rules = {}
            for coll in rules:
                nam, defs = coll.popitem()
                l = []
                for rul in defs:
                    rnam, rval = rul.popitem()
                    if rnam == '__ignore__':
                        l.append((re.compile(rval[0]), Action()))
                    else:
                        l.append((re.compile(rval[0]), Action(rval[1], rnam)))
                self.rules[nam] = l

        if type(source) == Lexer:
            init_as_lex()
        elif type(source) == text_reader.TextReader:
            init_as_text()
        else:
            raise Exception("Invalid source type: {}".format(type(source)))
    
    
    def is_end(self): # TODO valami hatékonyabb?
        return self.source.is_end()
    
    # Match mode
    # TODO pozíciók
    def _get_from_tr_(self):
        if len(self.buffer) < self.max_lex_len and not self.source.is_end(): # TODO is_end??
            self.buffer += self.source.read()
        
        for pat, act in self.rules:
            mtch = pat.match(self.buffer)
            if mtch:
                self.buffer = self.buffer[len(mtch.group()):] # TODO előző eltárolása a visszatekintés miatt?
                t = act.action(mtch.group(), self.row, self.column)
                if t: return t
                else: return self._get_from_tr_() # TODO átgondolni, hogy hatékony-e
                # TODO Ha a buf végére ért, nem biztos, hogy valid a találat, vagy nincs is találat. max_len nem kötelező!
        else:
            raise BufferError("No match found. {}".format(self.buffer[0:10]))
        
    
    
    # TODO pozíciók
    def _get_from_lx_(self):
        if not self.buffer and not self.source.is_end():
            self.tok = self.source.get_token()
            if self.tok[0] not in self.rules.keys():
                return self.tok
            
            self.buffer = self.tok[1]
            self.row = self.tok[2]
            self.column = self.tok[3]
            
            return self.tok
        
        for pat, act in self.rules[self.tok[0]]:
            mtch = pat.match(self.buffer)
            if mtch:
                self.buffer = self.buffer[len(mtch.group()):] # TODO előző eltárolása a visszatekintés miatt?
                t = act.action(mtch.group(), self.row, self.column)
                if t: return t
                else: return self._get_from_lx_()
        else:
            raise BufferError("No match found. {}".format(self.buffer[0:10]))
        
        








