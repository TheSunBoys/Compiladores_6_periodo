import urllib as req
from abc import ABC

class File(ABC):
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        return 1+1
    
    def math(self):
        return 2+4*3/6**10-2%6
    
    def why(self):
        option = 3
        match(option):
            case 3:
                return 'found value of option'
            case int(option):
                return 'found int'
            case str(option):
                return 'found string'
        if self.filename:
            return 'dale'
        else:
            return 'nope'

if __name__ == '__main__':
    with open('file.txt', 'r') as f:
        content = f.read()