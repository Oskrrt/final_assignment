from file_organizer.file_handler import FileHandler

def main():
    print("Hello World")
    fh = FileHandler()
   # fh.get_supported_file_types_from_config()
   # fh.get_files()
    #fh.reset_directory()
    fh.organize_files()

if __name__ == "__main__":
    main()