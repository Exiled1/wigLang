import pprint

class Logger:
    def __init__(self):
        self.entries = []
    def add(self, data):
        if type(data) is list:
            data = [s if type(s) is str else str(s) for s in data]
            self.entries.append(data)
        else:
            self.entries.append([data])
    
    def _print(self, changes=True):
        entries = [[l[0],l[1]] if changes else [l[0]] for l in self.entries]
        for lis in entries:
            print(*lis, sep=' | ')


logger_instance = Logger()
def log(*d):
    logger_instance.add([*d])

