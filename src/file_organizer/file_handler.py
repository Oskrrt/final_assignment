import tomllib
import os
import sys
from itertools import filterfalse
import shutil

from file_organizer.logger import logged

class FileHandler:
    CONFIG_FILE_PATH = os.path.join('src', 'file_organizer', 'file_config.toml')

    def __init__(self):
        print("cwd: " + os.getcwd())
        self.default_directory = os.path.join('src', 'file_organizer', 'directories')

    # resets the files in the directory to the default structure, used for testing the organizer.
    def reset_directory(self):
        dirs = [d for d in os.listdir(self.default_directory) if os.path.isdir(os.path.join(self.default_directory, d))]
        print(dirs)
        for dir in dirs:
            src_path = os.path.join(self.default_directory, dir)
            print(src_path)
            files_in_dir = os.listdir(src_path)
            for file in files_in_dir:
                shutil.move(os.path.join(src_path, file), os.path.join(self.default_directory, file))
            # was getting winerror 5, access denied on the directory deletion without ignore_errors=True
            shutil.rmtree(src_path, ignore_errors=True)

        #shutil.rmtree(os.path.join(self.default_directory, dirs[0]), ignore_errors=True)

    # the main method in the class which does the file organizing.
    def organize_files(self):
        files = self.get_files()
        print("Files before remove: " + str(files))
        files = self.remove_unsupported_files(files)
        print("Files after remove: " + str(files))
        for file in files:
            self.move_file(file)
        return ""

    def remove_unsupported_files(self, files):
        supported_file_types = self.get_supported_file_types_from_config()["filetypes"]
        print("supported file types: " + str(supported_file_types))
        for file in files:
            file_type = self.determine_file_type(file)
            print(file_type)
            if file_type not in supported_file_types:
                #print("unsupported file type")
                files.remove(file)
                self.remove_file(file)
        return files

    #@logged("delete")
    def remove_file(self, file):
        path = os.path.join(self.default_directory, file)
        if os.path.exists(path):
            os.remove(path)
            print("removed file: " + path)
        else:
            print("The file does not exist")

    #@logged("file moved")
    def move_file(self, file):
        file_type = self.determine_file_type(file)
        self.create_directory(file_type)
        print("file: " + file)
        src_path = os.path.join(self.default_directory, file)
        print("srcPath: " + src_path)
        dst_path = os.path.join(self.default_directory, file_type, file)
        print("dstPath: " + dst_path)
        shutil.move(src_path, dst_path)




    #@logged("directory created")
    def create_directory(self, dir_name):
        path = os.path.join(self.default_directory, dir_name)
        print("dir path: " + path)
        if not os.path.exists(path):
            os.makedirs(path)
        return ""

    def get_files(self):
        #return os.listdir(self.default_directory)
        files = os.listdir(self.default_directory)
        return [f for f in files if os.path.isfile(os.path.join(self.default_directory, f))]

    def log_event(self, event):
        return ""

    def determine_file_type(self, file):
        file_type = file.split(".")[1]
        #print(file_type)
        return file_type

    #@logged("error")
    def get_supported_file_types_from_config(self):
        with open(self.CONFIG_FILE_PATH, "rb") as f:
            #print(tomllib.load(f))
            return tomllib.load(f)["filetypes"]
