class ToDo:
    
    progress = 0 # class-level variable
    TYPE_KEY = 'T'

    def __init__(self, description, status):
        self.description = description
        self.is_done = status
        
    def __str__(self):        
        return self.__status_as_icon().center(6) + self.description.ljust(14)

    def mark_as_done(self):
        if not self.is_done: # increment progress if needed
            ToDo.progress = ToDo.progress + 1
        self.is_done = True

    def mark_as_pending(self):
        if self.is_done: # decrement progress if needed
            if ToDo.progress != 0:
                ToDo.progress = ToDo.progress - 1
        self.is_done = False

    def __status_as_icon(self):
        return 'X' if self.is_done else '-'
    
    def as_csv(self):
        """ Return the details of todo object as a list,
        suitable to be stored in a csv file.
        """
        return [self.TYPE_KEY, self.description, 'done' if self.is_done else 'pending']
    
    def as_item(self):
        """ Return the name of the item as a string."""
        return self.description