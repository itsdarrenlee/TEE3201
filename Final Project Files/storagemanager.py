# -*- coding: utf-8 -*-
import csv
import deadline as dl
import todo as td

class StorageManager:
    
    def __init__(self, filename):
        self.filename = filename
        
    def load_data(self, items):
        """
        Loads data from csv specified.
        
        If csv does not exist, a new CSV file is created
        in the same directory as main. 
        
        Items are loaded from CSV into the item list.

        Returns
        -------
        None.

        """
        self.__create_file_if_missing(self.filename)
        with open(self.filename, 'r') as csvfile:
            file_handler = csv.reader(csvfile)
            for row in file_handler:
                if not row:
                    continue
                self.__load_item_from_csv_line(row, items)
            return
        
    def __create_file_if_missing(self, filename):
        """
        Creates a file. 
        
        If the named csv file is locked for editing, a permission error is
        raised to console.

        Returns
        -------
        None.

        """
        try:
            open(filename, 'a').close()
        except PermissionError as pe:
            raise PermissionError("Error creating file, check permissions.") from pe
        
        
    def __load_item_from_csv_line(self, row, items):
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
                items.append(td.ToDo(row[1], True if row[2] == 'True' else False))
            elif row[0] == 'D':
                items.append(dl.Deadline(row[1], True if row[2] == 'True' else False, row[3]))
        except IndexError:
            raise IndexError
        return
    
    def save_data(self, items):
        """
        Method to save data to external CSV specified in attribute.

        Returns
        -------
        None.

        """
        with open(self.filename, "w", newline='') as csvfile:
            output = csv.writer(csvfile)
            for item in items:
                if isinstance(item, dl.Deadline):          
                    output_to_file = ["D",item.description,item.is_done,item.by]
                else:
                    output_to_file = ["T",item.description,item.is_done]
                output.writerow(output_to_file)