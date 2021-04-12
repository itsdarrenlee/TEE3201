import csv
import deadline as dl
import todo as td
import exceptions as ex
import re

class TaskManager:
    
    items = []
    filename = 'monty7.csv'
    
    def __init__(self):
        self.load_data()
        self.items = TaskManager.items
    
    def get_help(self):
        """
        Generates the list of commands available
        for T800.

        Returns
        -------
        None.

        """
        return """============================================
T800 can understand the following commands:

  todo DESCRIPTION 
    Adds a task to the list
    Example: todo read book
  deadline DESCRIPTION "by:" DEADLINE
    Adds a task with deadline to the list
    Example: deadline read book by: Tuesday
  done INDEX
    Marks the task at INDEX as 'done'
    Example: done 1
  delete INDEX
    Deletes item at the index
    Example: delete 1
  pending INDEX
    Reverts done item at index to 'pending'
    Example: pending 1
  exit
    Exits the application
  help
    Shows the help information
  progress
    Shows the progress of the current tasks
  mass TASK INDEX + **More if needed
    Performs either done, pending or delete
    of tasks simultaneously. 
    Space is required in between each task.
    Example: pending 1 3 4
--------------------------------------------"""
    
    def load_data(self):
        """
        Loads data from csv specified in Class attribute.
        
        If csv does not exist, a new CSV file is created
        in the same directory as main. 
        
        Items are loaded from CSV into the item list, a TaskManager attribute.

        Returns
        -------
        None.

        """
        TaskManager.__create_file_if_missing(self)
        with open(self.filename, 'r') as csvfile:
            file_handler = csv.reader(csvfile)
            for row in file_handler:
                if not row:
                    continue
                self.__load_item_from_csv_line(row)
            return

    def __create_file_if_missing(self):
        """
        Creates a file specified in TaskManager attribute. 
        
        If the named csv file is locked for editing, a permission error is
        raised to console.

        Returns
        -------
        None.

        """
        try:
            open(self.filename, 'a').close()
        except PermissionError as pe:
            raise PermissionError("Error creating file, check permissions.") from pe
        
        
    def __load_item_from_csv_line(self, row):
        """
        From the specified CSV, it will read the CSV row by row and create todo
        and deadline objects respectively.

        Parameters
        ----------
        row : Each line in CSV passed from csv_reader
            If CSV line starts with 'T', create ToDo instance, else
            if line starts with 'D', create Deadline instance.

        Raises
        ------
        IndexError
            Raises IndexError if unable to get indexes of row.

        Returns
        -------
        None.

        """
        try:
            if row[0] == 'T':
                self.items.append(td.ToDo(row[1], True if row[2] == 'True' else False))
            elif row[0] == 'D':
                self.items.append(dl.Deadline(row[1], True if row[2] == 'True' else False, row[3]))
        except IndexError:
            raise IndexError
        return
    
    def save_data(self):
        """
        Method to save data to external CSV specified in attribute.

        Returns
        -------
        None.

        """
        with open(self.filename, "w", newline='') as csvfile:
            output = csv.writer(csvfile)
            for item in self.items:
                if isinstance(item, dl.Deadline):          
                    output_to_file = ["D",item.description,item.is_done,item.by]
                else:
                    output_to_file = ["T",item.description,item.is_done]
                output.writerow(output_to_file)
    
    def add_item(self, user_input):
        """
        Adds a 'ToDo' type item into the local list.

        Parameters
        ----------
        user_input:
            All input after keyword 'todo' is considered valid.

        Raises
        ------
        IndexError
            If user provides blank input, indexerror will catch
            exception.

        Returns
        -------
        Prints to GUI information on task added.

        """
        command_parts = user_input.strip().split(' ', 1)
        try:
            self.items.append(td.ToDo(command_parts[1], False))
            return ("New item: " + "'" + command_parts[1] + "'" + " added")
        except IndexError as ie:
            raise IndexError("INPUT: todo \"task\"") from ie

            
    def add_deadline_item(self, user_input):
        """
        Adds a 'Deadline' type item into the list.

        Parameters
        ----------
        user_input : Requires a keyword 'by:'
            All input after keyword 'deadline' is considered valid.

        Raises
        ------
        InvalidDeadlineInput:
            When 'by' keyword is not present in input (case insensitive)
            
        NoTaskError:
            When no task is provided but 'by:' keyword is present
        
        NoDueDateError:
            When no due date is provided but 'by:' keyword is present
            
        NoDueNoTaskError:
            When both task & due date is not provided but keyword is present

        Returns
        -------
        Prints to GUI information on task added.

        """
        if re.search(" by:", user_input, re.IGNORECASE):
            command_parts = user_input.strip().split(' ', 1)
            arr = re.split("by:", command_parts[1], 1, re.IGNORECASE)
            (task, due) = [x.strip() for x in arr]
            
            if not due and not task:
                raise ex.NoDueNoTaskError("INPUT: deadline \"task\" by: \"due date\"")
            elif not due:
                raise ex.NoDueDateError("No due date provided! INPUT: deadline \"task\" by: \"due date\"" )
            elif not task:
                raise ex.NoTaskError("Provide a task! INPUT: deadline \"task\" by: \"due date\"")
    
            self.items.append(dl.Deadline(task, False, due))
            return ("New item: " + "'" + task + "'" + " added. " + "Deadline: " + "'" + due + "'")
        else:
            raise ex.InvalidDeadlineInput("Missing 'by' keyword! INPUT: deadline \"task\" by: \"due date\"")
            
    def mark_item_as_done(self, user_input):
        
        index_as_string = user_input[5:].strip()
        index_to_remove = self.__index_check(index_as_string)
        for i, obj in enumerate(self.items):
            if i == index_to_remove:
                if obj.is_done:
                    return ("Item: " + "'" + obj.description + "'" + " has been done already")
                obj.mark_as_done()
                return ("Item: " + "'" + obj.description + "'" + " marked as done")
            
    def mark_item_as_pending(self, user_input):
        index_as_string = user_input[8:].strip()
        index_to_remove = self.__index_check(index_as_string)
        for i, obj in enumerate(self.items):
            if i == index_to_remove:
                if not obj.is_done:
                    return ("Item: " + "'" + obj.description + "'" + " is already pending")
                obj.mark_as_pending()
                return ("Item: " + "'" + obj.description + "'" + " marked as pending")
    
    def __index_check(self, string):
        try:
            index = int(string.strip())
        except ValueError as ve:
            raise ValueError('"{}" is not a number'.format(string)) from ve
        if index < 1:
            raise ex.ZeroInputError('Index must be greater than 0')
        try:
            if self.items[index - 1]:
                return index - 1
        except IndexError as ie:
            raise IndexError('No item at index: {}'.format(string)) from ie
            
            
    def delete_item(self, user_input):
        try:
            s = int(user_input[7:].strip())
            if s == 0:
                raise IndexError
            deleted_item = self.items.pop(s-1)
            return ("Task: " + "'" + deleted_item.description + "'" + " deleted from the list")
        except IndexError:
            raise IndexError("There is no list item at the number you typed!")
        except ValueError:
            raise ValueError("Only integers accepted as input")
            
    def get_current_progress(self):
        status = {'Todo': 0, 'Deadline': 0}
        tFlag = 0
        dFlag = 0
        for obj in self.items:
            if isinstance(obj, dl.Deadline) and dFlag == 0:
                status['Deadline'] = obj.progress
                dFlag = 1
            elif tFlag == 0:
                status['Todo'] = obj.progress
                tFlag = 1
        return("""Progress for this session:
    | ToDos: {} | Deadlines: {} |""".format(status['Todo'], status['Deadline']))
    
    def mass(self, user_input):
        command = user_input[5:].strip()
        if re.search("\Adelete", command[:6], re.IGNORECASE):
            return self.mass_execute(command.lower(), self.delete_item, 7)
        elif re.search("\Adone", command[:4], re.IGNORECASE):
            return self.mass_execute(command.lower(), self.mark_item_as_done, 5)
        elif re.search("\Apending", command[:7], re.IGNORECASE):
            return self.mass_execute(command.lower(), self.mark_item_as_pending, 8)
        else:
            raise ex.InvalidMassInputError("INPUT: 'mass' + command + args**")
            
    def mass_execute(self, command, function_name, strip_len):
        string = command[strip_len:]
        back_string = command[:strip_len]
        str_arr = [int(s) for s in string.split() if s.isdigit()]
        str_arr.sort(reverse=True)
        for i in str_arr:
            self.execute_command(back_string + str(i))
        if str_arr:
            return ("Executed mass action '{}' on items {}!".format(back_string.strip(), [i for i in str_arr]))
        else:
            raise ex.InvalidMassInputError("Nothing was done! Check your input.")
        
    def execute_command(self, command):
        if re.search("\Ahelp", command[:4], re.IGNORECASE):
            return self.get_help()
        elif re.search("\Aprogress", command[:8], re.IGNORECASE):
            return self.get_current_progress()
        elif re.search("\Atodo", command[:4], re.IGNORECASE):
            return self.add_item(command)
        elif re.search("\Adeadline", command[:8], re.IGNORECASE):
            return self.add_deadline_item(command)
        elif re.search("\Adone", command[:4], re.IGNORECASE):
            return self.mark_item_as_done(command)
        elif re.search("\Apending", command[:7], re.IGNORECASE):
            return self.mark_item_as_pending(command)
        elif re.search("\Adelete", command[:6], re.IGNORECASE):
            return self.delete_item(command)
        elif re.search("\Amass", command[:4], re.IGNORECASE):
            return self.mass(command)
        else:
            raise Exception('Command not recognized')                 
