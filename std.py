import sys
 
class Logger:
 
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'a')
        self.file_enable = True
        
    def write(self, message):
        self.console.write(message)
        if self.file_enable:
            self.file.write(message)
 
    def flush(self):
        self.console.flush()
        self.file.flush()

    def fileEnable(self, val, newfile=None):
        self.file_enable = val
        if newfile:
            self.file.close
            self.file = open(newfile, 'a')

 
path = 'file.txt'
out = Logger(path)
sys.stdout = out
print('Hello, World1')
out.fileEnable(False)
print('Hello, World2')
out.fileEnable(True)
print('Hello, World3')
out.fileEnable(True, "file2.txt")
print('Hello, World4')