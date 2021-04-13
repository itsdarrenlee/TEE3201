import unittest
import exceptions as ex
import taskmanager as tm     

# test class
class TestSearch(unittest.TestCase):
    
    test_task_manager = tm.TaskManager()

    def test_add_item(self):
        with self.assertRaises(IndexError):
            self.test_task_manager.add_item("todo")
        with self.assertRaises(IndexError):
            self.test_task_manager.add_item("todo    ")
        self.assertEqual(self.test_task_manager.add_item("todo foo bar"), "New item: 'foo bar' added")
        self.assertEqual(self.test_task_manager.add_item("todo 1234567"), "New item: '1234567' added")
        self.assertEqual(self.test_task_manager.add_item("todo !@#$%^&*"), "New item: '!@#$%^&*' added")
        self.assertEqual(self.test_task_manager.add_item("todo todo"), "New item: 'todo' added")
        
    def test_add_deadline_item(self):
        self.assertEqual(self.test_task_manager.add_deadline_item("deadline foo by: bar")
                          , "New item: 'foo' added. Deadline: 'bar'")
        self.assertEqual(self.test_task_manager.add_deadline_item("deadline 123 by: 567")
                          , "New item: '123' added. Deadline: '567'")
        self.assertEqual(self.test_task_manager.add_deadline_item("deadline deadline by: deadline")
                          , "New item: 'deadline' added. Deadline: 'deadline'")
        self.assertEqual(self.test_task_manager.add_deadline_item("deadline !@#$% by:       ((*&^))      ")
                          , "New item: '!@#$%' added. Deadline: '((*&^))'")
     
        
        with self.assertRaises(ex.InvalidDeadlineInput):
            self.test_task_manager.add_deadline_item("deadline")
        with self.assertRaises(ex.NoTaskError):
            self.test_task_manager.add_deadline_item("deadline by: foo")
        with self.assertRaises(ex.NoDueDateError):
            self.test_task_manager.add_deadline_item("deadline foo by: ")
        with self.assertRaises(ex.NoDueNoTaskError):
            self.test_task_manager.add_deadline_item("deadline by: ")
        with self.assertRaises(ex.NoTaskError):
            self.test_task_manager.add_deadline_item("deadline by: by:")
        with self.assertRaises(ex.InvalidDeadlineInput):
            self.test_task_manager.add_deadline_item("deadline foo by")
        
# activate the test runner
if __name__ == '__main__':
    unittest.main()    
    
    
    