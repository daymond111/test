import os
import sys
import subprocess

CURRENT_DIRECTORY = os.path.abspath('./')
BUILT_IN_COMMANDS = ['echo', 'exit', 'type', 'pwd', 'cd']

def get_os_commands():
    if sys.platform.startswith('linux'):
        bin_dirs = ['/bin', '/usr/bin']
        commands = []
        for dir in bin_dirs:
            commands.extend(os.listdir(dir))
        return commands
    elif sys.platform.startswith('win'):
        paths = os.environ['PATH'].split(os.pathsep)
        commands = []
        for path in paths:
            commands.extend(os.listdir(path))
        return commands
    else:
        return []

def get_user_command():
    return input('$ ')

def find_executable_path(command):
    paths = os.environ['PATH'].split(os.pathsep)
    for path in paths:
        executable_path = os.path.join(path, command)
        if os.path.isfile(executable_path):
            return executable_path
    return None

def execute_built_in_command(command, arguments):
    global CURRENT_DIRECTORY
    match command:
        case 'exit':
            sys.exit(0)
        case 'echo':
            print(' '.join(arguments))
        case 'type':
            executable_path = find_executable_path(arguments[0])
            if arguments[0] in BUILT_IN_COMMANDS:
                print(f"{arguments[0]} is a shell builtin")
            elif executable_path:
                print(f"{arguments[0]} is {executable_path}")
            else:
                print(f"{arguments[0]}: not found")
        case 'pwd':
            print(CURRENT_DIRECTORY)
        case 'cd':
            if len(arguments) > 0:
                if arguments[0] == "~":
                    CURRENT_DIRECTORY = os.path.expanduser("~")
                else:
                    new_dir = arguments[0]
                    if os.path.isabs(new_dir):
                        CURRENT_DIRECTORY = os.path.abspath(new_dir)
                    else:
                        CURRENT_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, new_dir))
                if not os.path.isdir(CURRENT_DIRECTORY):
                    print(f"cd: {arguments[0]}: No such file or directory")
                    CURRENT_DIRECTORY = os.path.abspath('./')
            else:
                CURRENT_DIRECTORY = os.path.expanduser("~")



def execute_external_command(command, arguments):
    if command in BUILT_IN_COMMANDS:
        execute_built_in_command(command, arguments)
    elif command in OS_COMMANDS:
        executable_path = find_executable_path(command)
        if executable_path:
            try:
                subprocess.run([executable_path, *arguments], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
        else:
            print(f"{command}: not found")
    else:
        try:
            subprocess.run([command, *arguments], check=True)
        except FileNotFoundError:
            print(f"{command}: not found")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")


def main():
    global OS_COMMANDS, CURRENT_DIRECTORY
    OS_COMMANDS = get_os_commands()

    while True:
        user_input = get_user_command()
        command_parts = user_input.split()
        if command_parts:
            execute_external_command(command_parts[0], command_parts[1:])

if __name__ == "__main__":
    main()
