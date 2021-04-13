import datetime
from tkinter import Tk, Entry, Text, LEFT, RIGHT, END
import itertools
import sys
import deadline as dl
import taskmanager as tm
import userinterface as ui

class GUI:

    def __init__(self, task_manager):
        
        # create ui class instance
        self.ui_object = ui.UserInterface()
        
        self.task_manager = task_manager
        self.window = Tk()
        self.window.geometry('800x700')  # set Window size
        self.window.title('Task Terminator T800')  # set Window title

        self.input_box = Entry(self.window)  # create an input box
        self.input_box.pack(padx=5, pady=5, fill='x')  # make the input box fill the width of the Window
        self.input_box.bind('<Return>', self.command_entered)  # bind the command_entered function to the Enter key
        self.input_box.focus()  # set focus to the input box

        # add a text area to show the chat history
        self.history_area = Text(self.window, width="50")
        self.history_area.pack(padx=5, pady=5, side=LEFT, fill="y")
        self.output_font = ('Courier New', 11)
        self.history_area.tag_configure('error_format', foreground='red', font=self.output_font)
        self.history_area.tag_configure('success_format', foreground='green', font=self.output_font)
        self.history_area.tag_configure('normal_format', font=self.output_font)

        # add a text area to show the list of tasks
        self.list_area = Text(self.window)
        self.list_area.pack(padx=5, pady=5, side=RIGHT, fill="both")
        self.list_area.tag_configure('normal_format',  font=self.output_font)
        self.list_area.tag_configure('pending_format', foreground='red', font=self.output_font)
        self.list_area.tag_configure('done_format', foreground='green', font=self.output_font)

        # show the welcome message and the list of tasks
        self.update_chat_history('start', 'Welcome to T800!', 'success_format')
        self.update_task_list(self.task_manager.items, self.ui_object)

    def update_chat_history(self, command, response, status_format):
        """
        status_format: indicates which color to use for the status message
          can be 'error_format', 'success_format', or 'normal_format'
        """
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_area.insert(1.0, '-' * 40 + '\n', 'normal_format')
        self.history_area.insert(1.0, '>>> ' + str(response) + '\n', status_format)
        self.history_area.insert(1.0, 'You said: ' + str(command) + '\n', 'normal_format')
        self.history_area.insert(1.0, current_time + '\n', 'normal_format')
    
    def update_task_list(self, tasks, ui_object):
        
        self.list_area.delete('1.0', END)  # clear the list area
        self.list_area.insert(END, self.ui_object.show_greeting())
        if len(tasks) == 0:
            self.list_area.insert(END, '>>> Nothing to list', 'normal_format')
        else:
            self.__overflow_print(tasks)            
    
    def __overflow_print(self, tasks):
        for i, task in enumerate(tasks):
            output_format = 'done_format' if task.is_done else 'pending_format'
            
            deadline_arr = []
            desc_arr = []
            
            if isinstance(task, dl.Deadline):
                to_print = str(task)[:6] + '|' + str(i+1).center(6) + '| ' + str(task)[6:20] + \
                ' | ' + str(task.by)[:8] + '\n'
                self.list_area.insert(END, to_print, output_format) # print first 8 chars of 'deadline' only
                
                if len(str(task.by)) > 8:
                    deadline_arr = self.__string_splitter(deadline_arr, task.by, 8) [1:] # if longer than 8 char, split string
            else:
                to_print = str(task)[:6] + '|' + str(i+1).center(6) + '| ' + str(task)[6:20] + \
                ' | ' + '-' + '\n'
                self.list_area.insert(END, to_print, output_format) # print first 14 chars of 'deadline' only
        
            if len(str(task.description)) > 14:
                desc_arr = self.__string_splitter(desc_arr, task.description, 14)[1:] # if longer than 14 char, split string

            for combination in itertools.zip_longest(desc_arr, deadline_arr, fillvalue=""):                    
                to_print = " "*15 + combination[0].ljust(14) + " "*3 + combination[1].ljust(8)  + '\n'
                self.list_area.insert(END, to_print, output_format) # iterate thru 2 lists simultanously, filling up diff with ""
        self.list_area.insert(END, """----------------------------------------------\n""")
        
    
    def __string_splitter(self, arr, string, split_length):
        """ Recursively splits the string greedily in length specified by split_length"""
        if len(string) < split_length:
            arr.append(string)
            return arr
        else:
            arr.append(string[:split_length])
            return self.__string_splitter(arr, string[split_length:], split_length)
    
    def clear_input_box(self):
        self.input_box.delete(0, END)
    
    def command_entered(self, event):
        command = None
        try:
            command = self.input_box.get().strip()
            if command.lower() == 'exit':
                self.window.destroy()
                sys.exit()
            output = self.task_manager.execute_command(command)
            self.update_chat_history(command, output, 'success_format')
            self.update_task_list(self.task_manager.items, self.ui_object)
            self.clear_input_box()
            self.task_manager.save_data()
        except Exception as e:
            self.update_chat_history(command, str(e), 'error_format')

    def start(self):
        self.window.mainloop()
        
if __name__ == '__main__' :
    GUI(tm.TaskManager()).start()