import tomllib
import os
import shutil

from file_organizer.logger import logged, log_error

class FileHandler:
    CONFIG_FILE_PATH = os.path.join('src', 'file_organizer', 'file_config.toml')
    DEFAULT_DIRECTORY = os.path.join('src', 'file_organizer', 'directories')
    TEXT_COLORS = {
        "green": '\033[92m',
        "orange": '\033[93m',
        "red": '\033[91m',
        "blue": '\033[94m'
    }
    
    # resets the files in the directory to the default structure, used for testing the organizer.
    @classmethod
    @logged("directory reset")
    def reset_directory(cls):
        directories = [d for d in os.listdir(cls.DEFAULT_DIRECTORY) if os.path.isdir(os.path.join(cls.DEFAULT_DIRECTORY, d))]
        #print(directories)
        for directory in directories:
            src_path = os.path.join(cls.DEFAULT_DIRECTORY, directory)
            files_in_dir = os.listdir(src_path)
            for file in files_in_dir:
                shutil.move(os.path.join(src_path, file), os.path.join(cls.DEFAULT_DIRECTORY, file))
            # was getting winerror 5, access denied on the directory deletion without ignore_errors=True
            shutil.rmtree(src_path, ignore_errors=True)
        print(f"{cls.TEXT_COLORS["green"]}The directory has been reset")
        #shutil.rmtree(os.path.join(cls.DEFAULT_DIRECTORY, dirs[0]), ignore_errors=True)

    # the main method in the class which does the file organizing.
    @classmethod
    def organize_files(cls):
        files = cls.get_files()
        if not files:
            print(f"{cls.TEXT_COLORS["green"]}No files to organize")
            return
        files = cls.remove_unsupported_files(files)
        try:
            for file in files:
                cls.move_file(file)
            print(f"{cls.TEXT_COLORS["green"]}The directory has been organized")
        except Exception as e:
            log_error(e)

    # Removes any unsupported files.
    @classmethod
    def remove_unsupported_files(cls, files):
        supported_file_types = cls.get_supported_file_types_from_config()["filetypes"]
        for file in files:
            file_type = cls.determine_file_type(file)
            if file_type not in supported_file_types:
                files.remove(file)
                cls.remove_file(file)
        return files

    @classmethod
    @logged("delete")
    def remove_file(cls, file):
        path = os.path.join(cls.DEFAULT_DIRECTORY, file)
        if os.path.exists(path):
            os.remove(path)
            print(f"{cls.TEXT_COLORS["red"]}removed file with unsupported filetype: " + path)
        else:
            print("The file does not exist")

    # moves a file from the default directory into the correct folder based on filetype.
    @classmethod
    @logged("file moved")
    def move_file(cls, file):
        file_type = cls.determine_file_type(file)
        src_path = os.path.join(cls.DEFAULT_DIRECTORY, file)
        #print("srcPath: " + src_path)
        dst_path = os.path.join(cls.DEFAULT_DIRECTORY, file_type, file)
        #print("dstPath: " + dst_path)
        new_dir_path = os.path.join(cls.DEFAULT_DIRECTORY, file_type)
        try:
            if not os.path.exists(new_dir_path):
                cls.create_directory(new_dir_path)

            shutil.move(src_path, dst_path)
            print(f"{cls.TEXT_COLORS["orange"]}moved file: " + file + " from " + src_path + " to " + dst_path)
        except Exception as e:
            log_error(e)

    @classmethod
    @logged("directory created")
    def create_directory(cls, path):
        os.makedirs(path)
        print(f"{cls.TEXT_COLORS["blue"]}created directory: " + path)

    # Fetches all files in the default directory
    @classmethod
    def get_files(cls):
        files = os.listdir(cls.DEFAULT_DIRECTORY)
        # the below line makes sure the returned list only contains files and not directories
        return [f for f in files if os.path.isfile(os.path.join(cls.DEFAULT_DIRECTORY, f))]

    #@classmethod
    #def test_error(cls):
        #log_error(e)
        #try:
            #raise Exception("Dette er en excpetion")
            #hei = "ba.le".split(".")
            #print("hei[2]")
        #except Exception as e:
            #print("hei", file=sys.stderr)
            #print(traceback.extract_stack())
            #print(format_stack())
            ##print(exc)


    # @classmethod
    # def log_error(cls, e):
    #     function_name = inspect.currentframe().f_back.f_code.co_name
    #     file_name = inspect.currentframe().f_code.co_filename
    #     print(function_name)
    #     code_block = '''
    #     @logged("error")
    #     def log_error_ast(e, function_name, file_name):
    #         message = "Error: " + str(e) + " occurred in method: " + function_name + " in file: " + file_name
    #         print(message, file=sys.stderr)
    #
    #     log_error_ast(e, function_name, file_name)
    #     '''
    #     code_block = textwrap.dedent(code_block)
    #     parsed_code_block = ast.parse(code_block, mode='exec')
    #     compiled_code = compile(parsed_code_block, '<string>', 'exec')
    #     # Execute the compiled code
    #     exec(compiled_code)


    #@classmethod
    # @logged("error")
    # def log_error_2(cls, e):
    #     function_name = inspect.currentframe().f_back.f_back.f_code.co_name
    #     file_name = inspect.currentframe().f_code.co_filename
    #     message = "Error: " + repr(e) + " occurred in method: " + function_name + " in file: " + file_name
    #     print(message, file=sys.stderr)
    #     #raise e

    # Determines the filetype based on what comes after "."
    @classmethod
    def determine_file_type(cls, file):
        file_type = file.split(".")[1]
        return file_type

    # Fetches all supported file types configured in the file_config.toml file
    @classmethod
    def get_supported_file_types_from_config(cls):
        try:
            with open(cls.CONFIG_FILE_PATH, "rb") as f:
                return tomllib.load(f)["filetypes"]
        except Exception as e:
            log_error(e)

