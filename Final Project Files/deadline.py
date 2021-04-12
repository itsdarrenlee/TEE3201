import todo as td

class Deadline (td.ToDo):
    
    _progress = 0 # class-level variable
    TYPE_KEY = 'D'

    def __init__(self, description, status, by):
        super().__init__(description, status)
        self.by = by        
    
    def __str__(self):
        s = super().__str__()
        return s[:-1] + " " + self.by
        
    def as_csv(self):
        c = super().as_csv()
        c.append(self.by)
        return c
        
    def mark_as_done(self):
        if not self.is_done: # increment progress if needed
            Deadline._progress = Deadline._progress + 1
        self.is_done = True
        
    def mark_as_pending(self):
        if self.is_done: # decrement progress if needed
            if Deadline._progress != 0:
                Deadline._progress = Deadline._progress - 1
        self.is_done = False