import os
import sys, importlib

INPUT_PROMPT = "Input the number of your choice, and press 'enter' to confirm your choice: "
def main():
    print("Choose the package to run:")
    print("1. Route Planner")
    print("2. File Organizer")
    chosen_package = input(INPUT_PROMPT)
    if chosen_package == '1':
        run_tarjan_planner()
    elif chosen_package == '2':
        run_file_organizer()
    else:
        exit("Invalid choice. Please choose a valid package.")

def run_tarjan_planner():
    print("\033[1m\033[4m\n-------------- Starting tarjan planner --------------\n\033[0m")
    runnable = dynamic_import(".route_planner", "tarjan_planner")
    runnable.init_route_planner()

def run_file_organizer():
    print(f"\033[1m\033[4m\nYou have chosen the file organizer.\033[0m")
    print("Select the option you want to run: ")
    print("1. Organize the files in the directory into folders")
    print("2. Reset the directory back to its default state")

    chosen_option = input(INPUT_PROMPT)
    runnable = dynamic_import(".file_handler", "file_organizer", "FileHandler")
    print("\033[1m\033[4m\n-------------- Starting file organizer --------------\n\033[0m")
    if chosen_option == '1':
        runnable.organize_files()
    elif chosen_option == '2':
        runnable.reset_directory()
    else:
        print("Invalid choice. Please choose a valid option.", file=sys.stderr)

# imports the modules for the package about to be run
# because FileHandler is a class and route_planner is not they need different handling.
def dynamic_import(module_name, package_name, module_class=None):
    runnable = importlib.import_module(module_name, package_name)
    if module_class:
        runnable = getattr(runnable, module_class)
        return runnable
    return runnable

if __name__ == "__main__":
    main()