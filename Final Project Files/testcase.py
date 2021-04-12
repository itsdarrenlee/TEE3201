import unittest
import todo as td
import deadline as dl
import exceptions as ex
import re

items = []

# check for 'todo' is done at an earlier stage. It is assumed
# that user_input for add_item() will be prefixed with 'todo'

def add_item(user_input):
       command_parts = user_input.strip().split(' ', 1)
       try:
           items.append(td.ToDo(command_parts[1], False))
           return ("New item: " + "'" + command_parts[1] + "'" + " added")
       except IndexError as ie:
           raise IndexError("INPUT: todo \"task\"") from ie
          
def add_deadline_item(user_input):
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
            
            
        items.append(dl.Deadline(task, False, due))
        return ("New item: " + "'" + task + "'" + " added. " + "Deadline: " + "'" + due + "'")
    else:
        raise ex.InvalidDeadlineInput("Missing 'by' keyword! INPUT: deadline \"task\" by: \"due date\"")         

# test class
class TestSearch(unittest.TestCase):
    
    def test_add_item(self):
        with self.assertRaises(IndexError):
            add_item("todo")
        with self.assertRaises(IndexError):
            add_item("todo    ")
        self.assertEqual(add_item("todo foo bar"), "New item: 'foo bar' added")
        self.assertEqual(add_item("todo 1234567"), "New item: '1234567' added")
        self.assertEqual(add_item("todo !@#$%^&*"), "New item: '!@#$%^&*' added")
        self.assertEqual(add_item("todo todo"), "New item: 'todo' added")
        
    def test_add_deadline_item(self):
        self.assertEqual(add_deadline_item("deadline foo by: bar")
                         , "New item: 'foo' added. Deadline: 'bar'")
        self.assertEqual(add_deadline_item("deadline 123 by: 567")
                         , "New item: '123' added. Deadline: '567'")
        self.assertEqual(add_deadline_item("deadline deadline by: deadline")
                         , "New item: 'deadline' added. Deadline: 'deadline'")
        self.assertEqual(add_deadline_item("deadline !@#$% by:       ((*&^))      ")
                         , "New item: '!@#$%' added. Deadline: '((*&^))'")
     
        
        with self.assertRaises(ex.InvalidDeadlineInput):
            add_deadline_item("deadline")
        with self.assertRaises(ex.NoTaskError):
            add_deadline_item("deadline by: foo")
        with self.assertRaises(ex.NoDueDateError):
            add_deadline_item("deadline foo by: ")
        with self.assertRaises(ex.NoDueNoTaskError):
            add_deadline_item("deadline by: ")
        with self.assertRaises(ex.NoTaskError):
            add_deadline_item("deadline by: by:")
        with self.assertRaises(ex.InvalidDeadlineInput):
            add_deadline_item("deadline foo by")
        
# activate the test runner
if __name__ == '__main__':
    unittest.main()    