# -*- coding: utf-8 -*-

class UserInterface():
    
    def __init__(self):
        return

    def show_greeting(self):
        return ("""           ______         __                  
          /_  __/__ ____ / /__                
           / / / _ `(_-</  '_/                
  ______  /_/  \_,_/___/_/\_\     __          
 /_  __/__ ______ _  (_)__  ___ _/ /____  ____
  / / / -_) __/  ' \/ / _ \/ _ `/ __/ _ \/ __/
 /_/  \__/_/ /_/_/_/_/_//_/\_,_/\__/\___/_/   
\n==============================================
STATUS | INDEX | DESCRIPTION      | DEADLINE
----------------------------------------------\n""")
        

    @staticmethod
    def get_help():
        """
        Generates the list of commands available
        for T800.

        Returns
        -------
        None.

        """
        return(""" I'm glad you asked. Here it is:
========================================
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
  find TASK
    Searchs the task list for tasks
    matching your description.
    Results are case-insensitive!
  wipe
    Clears all tasks from the task pane. This action
    is permanent!
==========================================""")