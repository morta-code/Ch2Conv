#!/usr/bin/python3

import re
import text_reader

####################################################################################################

class Action:
    """ Action osztály a találatok kezelésére
    Action(**args)
        Action konstruktor. Argumnetumkulcsok:
        token_name: Token-név, str, kötelező
        value_needed: A token tárolja-e a felismert lexémát? bool
        external_call: Külső függvény hívása a lexéma utófeldolgozására. str
             A külső függvény szignatúrája:  fuction_name(found_lexeme): str
        module: Modul elérési útja. Ha van external_call, kötelező. str
    self.action(match_str, row, column) : tuple
        A talált lexémára létrehozza a megfelelő tokent
    """
    def __init__(self, **args):
        """
        self.token_name
        self.action
        self.external_call
        """
        self.token_name = args['token_name']
        v = args.get('value_needed', True)
        self.action = _action_with_v if v else _action_without_v
        self.external_call = args.get('external', None)
        if self.external_call:
            self.action = _action_with_external_call
            #self.mod = importlib.import_module(args['module']) # todo javítás
            runfile(args['module'])
            self.external_call = locals()[self.external_call]
    
    def _action_with_v(self, match_str, row, column):
        return (self.token_name, match_str, row, column)
    
    def _action_withtout_v(self, match_str, row, column):
        return (self.token_name, None, row, column)

    def _action_with_external_call(self, match_str, row, column):
        match_str = self.external_call(match_str) #getattr(self.mod, self.external_call)(match_str)
        return (self.token_name, match_str, row, column)
    
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
        self.rules = [] # TODO
        self.row = 0
        self.column = 0
        
        def init_as_text():
            self.get_token = self._get_from_tr_
            self.buffer = source.read()
            self.max_lex_len = None # TODO
        
        def init_as_lex():
            self.get_token = self._get_from_lx_
            self.tok = None
            
        
        if type(source) == Lexer: init_as_lex()
        elif type(source) == text_reader.TextReader: init_as_text()
        else: raise Exception("Invalid source type: {}".format(type(source)))
        
#         self.buffer = None
#         self.r_list = list()
#         self.limit = 10 #default max token hossz
#         self.source = source
#         self.s_type_l = True
#         self.load_from_s = None
#         self.end_of_source = False
#         def build(k,v):
#             """
#             Szabályt felépítő eljárás
#             """
#             if k == '__maxlength__':
#                 self.limit = v
#                 return
#             if type(v) == list:
#                 flags = 0
#                 if 'i' in v[1] : flags |= re.IGNORECASE
#                 if 'u' in v[1] : flags |= re.UNICODE
#                 if 'a' in v[1] : flags |= re.ASCII
#                 self.r_list.append( (re.compile(v[0], flags), k) )
#             else:
#                 self.r_list.append( (re.compile(v), k) )
#         
#         if type(source) == Lexer:
#             self.s_type_l = True
#             self.load_from_s = self._get_from_lx_
#         elif type(source) == text_reader.TextReader:
#             self.s_type_l = False
#             self.load_from_s = self._get_from_tr_
#         else: raise Exception("Not valid source type: {}. Lexer or TextReader expected".format(type(source)))
#         
#         if type(rules) == dict:
#             for key,val in rules.items():
#                 build(key, val)
#         elif type(rules) == list:
#             for r in rules:
#                 key,val = r.popitem()
#                 build(key, val)
#         else: raise Exception("Not valid argument: {}. Expected dict of token definitions or list of list of name, def pairs".format(type(rules)))
        
    
    def is_end(self): # TODO
        pass
    
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
        # TODO átgondolni, hogyan tárolom a szabályokat
        if not self.buffer and not self.source.is_end():
            self.tok = self.source.get_token()
            if self.tok[0] not in self.rules.keys():
                return self.tok
            
            self.buffer = self.tok[1]
            self.row = self.tok[2]
            self.column = self.tok[3]
        
        for pat, act in self.rules[self.tok[0]]:
            mtch = pat.match(self.buffer)
            if mtch:
                self.buffer = self.buffer[len(mtch.group()):] # TODO előző eltárolása a visszatekintés miatt?
                t = act.action(mtch.group(), self.row, self.column)
                if t: return t
                else: return self._get_from_lx_()
                
        else: raise BufferError("No match found. {}".format(self.buffer[0:10]))
        
        








