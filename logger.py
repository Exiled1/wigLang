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

class FinalLogger:
    def __init__(self):
        self.entries = []
        self.depth = 0
    def add(self, data):
        if type(data) is list:
            data = [s if type(s) is str else str(s) for s in data]
            self.entries.append(data)
        elif type(data) is str:
            self.entries.append(data)
        else:
            self.entries.append([data])
    
    def _print(self, changes=True): 
        #.add passes a singleton list wrapped in a tuple.
        entries = self.entries
        
        for lis in entries:
            if type(lis) is list:
                del lis[1] # this contains the object for debug logging.
            tabs = lambda d:"\t".join(''for i in range(d))
            # if type(lis) is tuple:
            #     lis = list(lis)
            #     del lis[1]
            if(type(lis) is str and lis == "push"):
                self.depth += 1
                print(tabs(self.depth), ">>")
                continue
            elif(type(lis) is str and lis == "pop"):
                print(tabs(self.depth), "<<")
                self.depth -= 1
                continue
            print(tabs(self.depth), *lis)
            #print(*lis, sep=' | ')
    def stack_push(self):
        self.add("push")
    def stack_pop(self):
        self.add("pop")

logger_instance = Logger()
final_log_inst = FinalLogger()

def log(*d):
    final_log_inst.add([*d])
    logger_instance.add([*d])

