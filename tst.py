import os

def rename_file(abs_path, new_name):
    
    directory, old_name = os.path.split(abs_path)
    print(directory)
    new_abs_path = os.path.join(directory, new_name)
    # Переименовываем файл
    os.rename(abs_path, new_abs_path)
    
    
    
old_path = "C:\\!!uploads\\b71c4e1b-c14d-4401-b69f-56bdabf37928\\jopa.txt"
new_path = "C:\!!uploads\b71c4e1b-c14d-4401-b69f-56bdabf37928\text.txt"
rename_file(old_path, "string.txt")