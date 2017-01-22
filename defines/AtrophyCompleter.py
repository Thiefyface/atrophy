import glob
import readline
import rlcompleter
import atexit

HISTLEN = 200
HISTFILE = ".atrophy-history"
DEFAULT_HIST_DISPLAY_LEN = 20

class AtrophyCompleter(rlcompleter.Completer):
     def __init__(self,cmdcomplete):
        self.text = ""
        self.matches = []
        self.cmdcomplete = cmdcomplete
        self.symbols = []
        self.index = 0
    
        self.last_run_start = -1

        self.delims = readline.get_completer_delims()
        readline.set_completer_delims(self.delims.replace("/",''))
        self.delims = readline.get_completer_delims()
        readline.set_completer_delims(self.delims.replace("?",''))
        self.delims = readline.get_completer_delims()
        readline.set_completer_delims(self.delims.replace("@",''))
        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.complete)

        readline.set_history_length(HISTLEN)
        try:
            readline.read_history_file(HISTFILE)
        except Exception as e:
            pass  

        atexit.register(self.on_exit)

     def on_exit(self):
        # append 'run'/'attach' to end for convieniance
        for i in range(readline.get_current_history_length(),0,-1):
            line = readline.get_history_item(i)
            if line.startswith("run") or line.startswith("attach"): 
                readline.add_history(line) 
                self.last_run_start = (readline.get_current_history_length() - i)
                break
        readline.write_history_file(HISTFILE)
        
     def print_history(self,count=0):
        buf = ""
        length = readline.get_current_history_length()
        if count == 0:
            count = DEFAULT_HIST_DISPLAY_LEN
        for i in range(length,length-count,-1):
            buf += readline.get_history_item(i)
            buf += "\n"
        return buf
    
     def addSymbols(self,symbols):
        for i in symbols:
            try:
                int(i)
            except:
                self.symbols.append(i)

     def complete(self,text,index):
        if text != self.text or not text:
            self.text = text
            if not readline.get_begidx():
                self.matches = [ w for w in self.cmdcomplete if w.startswith(text) ]
            else:
                context = readline.get_line_buffer().split(" ")
                #check first word, see if it's an atrophy command
                
                
                if context[0] in self.cmdcomplete and context[0] != "run":
                    self.matches = [ s for s in self.symbols if s.startswith(text)]
                else:
                    self.matches = [ f for f in glob.glob(context[-1]+'*')]
        else:
            try:
                return self.matches[index]
            except:
                pass
        try:
            return self.matches[index]
        except:
            return None
