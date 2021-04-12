import re
import deadline as dl
import todo as td
import exceptions as ex
import storagemanager as sm

filename = 'monty7.csv'

class TaskManager:
    
    filename = 'monty7.csv'
    items = []
    
    def __init__(self):
        self.storage = sm.StorageManager(filename)
        self.storage.load_data(self.items)
    
    def save_data(self):
        self.storage.save_data(self.items)
        
    def get_help(self):
        """
        Generates the list of commands available
        for T800.

        Returns
        -------
        None.

        """
        return """========================================
T800 can understand the following commands:
(Case-insensitive)

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
============================================"""
    
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
            If user provides blank input

        Returns
        -------
        Information on task added.

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
        ex.InvalidDeadlineInput:
            When 'by' keyword is not present in input (case insensitive)
            
        ex.NoTaskError:
            When no task is provided but 'by:' keyword is present
        
        ex.NoDueDateError:
            When no due date is provided but 'by:' keyword is present
            
        ex.NoDueNoTaskError:
            When both task & due date is not provided but keyword is present

        Returns
        -------
        Information on task added.

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
        """
        Marks a specified item as 'done'.

        Parameters
        ----------
        user_input : 
            A number within bounds of the current tasklist.

        Returns
        -------
        Information on task marked 'done' or if task has been mark 'done' prior.

        """
        
        index_as_string = user_input[5:].strip()
        index_to_remove = self.__index_check(index_as_string)
        for i, obj in enumerate(self.items):
            if i == index_to_remove:
                if obj.is_done:
                    return ("Item: " + "'" + obj.description + "'" + " has been done already")
                obj.mark_as_done()
                return ("Item: " + "'" + obj.description + "'" + " marked as done")
            
    def mark_item_as_pending(self, user_input):
        """
        Marks a specified item as 'pending'.

        Parameters
        ----------
        user_input : 
            A number within bounds of the current tasklist.

        Returns
        -------
        Information on task marked 'pending' or if task has been mark 'pending' prior.

        """
        index_as_string = user_input[8:].strip()
        index_to_remove = self.__index_check(index_as_string)
        for i, obj in enumerate(self.items):
            if i == index_to_remove:
                if not obj.is_done:
                    return ("Item: " + "'" + obj.description + "'" + " is already pending")
                obj.mark_as_pending()
                return ("Item: " + "'" + obj.description + "'" + " marked as pending")
    
    def __index_check(self, string):
        """
        Helper function to check for valid input for mark_as_done and
        mark_as_pending methods.

        Parameters
        ----------
        string : 
            A single number that was obtained from input of the mark_as_done
            or mark_as_pending functions

        Raises
        ------
        ValueError
            Non-numerical input.
        ex.ZeroInputError:
            Invalid element '0' specified
        IndexError
            No element at specified index.

        Returns
        -------
        Provided number - 1

        """
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
        """
        Deletes item from local tasklist.

        Parameters
        ----------
        user_input :
            A number within bounds of the current tasklist.

        Raises
        ------
        IndexError
            No element at specified index.
        ValueError
            Non-numerical input.

        Returns
        -------
        Information on task deleted.

        """
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
        """
        Obtains progress of current session, ie.
        how many ToDos and Deadlines tasks marked as done.
        Tasks marked pending after being marked done will be
        taken into account.

        Returns
        -------
        Progress for this session.

        """
        status = {'Todo': 0, 'Deadline': 0}
        status['Todo'] = td.ToDo.progress_check()
        status['Deadline'] = dl.Deadline.progress_check()
        return("""Progress for this session:
    | ToDos: {} | Deadlines: {} |""".format(status['Todo'], status['Deadline']))
    
    def mass(self, user_input):
        """
        Executes mass execution of delete, pending or done sub methods.

        Parameters
        ----------
        user_input :
            Requires either 'delete', 'done', or 'pending' to be specified.

        Raises
        ------
        ex.InvalidMassInputError
            When action keywords 'delete', 'pending', or 'done' is not specified

        Returns
        -------
        A internal call to private method mass_execute.

        """
        command = user_input[5:].strip()
        if re.search("\Adelete", command[:6], re.IGNORECASE):
            return self.__mass_execute(command.lower(), self.delete_item, 7)
        elif re.search("\Adone", command[:4], re.IGNORECASE):
            return self.__mass_execute(command.lower(), self.mark_item_as_done, 5)
        elif re.search("\Apending", command[:7], re.IGNORECASE):
            return self.__mass_execute(command.lower(), self.mark_item_as_pending, 8)
        else:
            raise ex.InvalidMassInputError("INPUT: 'mass' + command + args**")
            
    def __mass_execute(self, command, function_name, strip_len):
        """
        Executes 'function_name' with parameters 'command' sequentially.
        Will execute all numbers regardless of whether input contains non-numerical
        input or not. 
        
        E.g. 'mass done 1 e3 app0e 2' results in task 1 and 2 marked as done.

        Parameters
        ----------
        command : Number
            Numbers to execute operations on
        function_name : method
            String representing method to execute
        strip_len : Number
            Length of string to strip()

        Raises
        ------
        ex.InvalidMassInputError
            if no numbers are supplied BUT keyword is present, e.g. 
            'mass delete abce1de'

        Returns
        -------
        Information on task and what was executed on.

        """
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
        """
        Main function to execute commands. All commmands are case-insensitive,
        i.e. 'DeAdlIne read book BY: 2pm' will add a Deadline item into list
        with a deadline of 2pm.

        Parameters
        ----------
        command : String
            User input from GUI box using Tkinter

        Raises
        ------
        Exception
            If command entered is not valid.

        Returns
        -------
        A call to associated command to execute with keyword parameters.

        """
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
            raise Exception('Command not recognized. Input \'help\' to see all available commands.')                 
