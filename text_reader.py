#!/usr/bin/python3


class TextReader:
    def __init__(self, stream, buffsize=4096):
        self._stream = stream
        self._buffersize = buffsize
        self._end = False
    
    def __iter__(self):
        while not self._end:
            yield self.read()
    
    def read(self):
        strng = self._stream.read(self._buffersize)
        if len(strng) < self._buffersize: self._end = True
        return strng
    
    def is_end(self):
        return self._end
