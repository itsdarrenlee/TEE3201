import unittest

def add_item(user_input):
        command_parts = user_input.strip().split(' ', 1)
        try:
            self.items.append(ToDo(command_parts[1], False))
            return ("New item: " + "'" + command_parts[1] + "'" + " added")
        except IndexError:
                raise IndexError("INPUT: todo \"task\"")
            
class TestSearch(unittest.TestCase):
    
    def test_add_item(self):
        
        
                
    def test_add_deadline_item(self):
        
# activate the test runner
if __name__ == '__main__':
    unittest.main()