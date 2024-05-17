import xml.etree.ElementTree as ET
import os

class SupportFunctions:
    def __init__(self):
        pass

    # Use following code to decide if this is a list of test names or test number 
    def check_list_type(self,lst):
        if isinstance(lst, list):
            if all(isinstance(item, (int, float)) for item in lst):
                return "List of numbers"
            elif all(isinstance(item, str) for item in lst):
                return "List of strings"
            elif len(lst)==0:
                return "Empty List"
            else:
                return "Mixed type list"
        else:
            return "Not a list"
        
    # Use following code to verify if it is a valid XML file with path
    def is_valid_xml_file(self,file_path):
        # Check if the file exists
        if not os.path.isfile(file_path):
            return False, "File does not exist"

            # Check if the file has .xml extension
        if not file_path.lower().endswith('.xml'):
            return False, "File is not an XML file"

            # Try to parse the XML file
        try:
            ET.parse(file_path)
        except ET.ParseError:
            return False, "Invalid XML content"
        return True, "Valid XML file"

    def windows_to_wsl_path(self,path):
        if path.startswith("\\") or (len(path) > 2 and path[1] == ":"):
            # Convert backslashes to forward slashes
            wsl_path = path.replace("\\", "/")
                
            # Convert drive letter to lowercase and prepend '/mnt/'
            wsl_path = "/mnt/" + wsl_path[0].lower() + wsl_path[2:]
                
            return wsl_path
        elif path.startswith("/mnt/"):
            return path
        else:
            return path




  