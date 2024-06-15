import os
import sys

BUILT_IN_COMMANDS = ['echo', 'exit', 'type']
PATHS = os.environ['PATH'].split(os.pathsep)

def get_user_input():
    return input('$ ')

def find_program_path(command):
    for path in PATHS:
        program_path = os.path.join(path, command)
        if os.path.isfile(program_path):
            return program_path
    return None

def execute_built_in_command(command, args):
    match command:
        case 'exit':
            sys.exit(0)
        case 'echo':
            print(' '.join(args))
        case 'type':
            if args[0] in BUILT_IN_COMMANDS:
                print(f"{args[0]} is a shell builtin")
            else:
                program_path = find_program_path(args[0])
                if program_path:
                    print(f"{args[0]} is {program_path}")
                else:
                    print(f"{args[0]}: not found")

def execute_external_command(command, args):
    program_path = find_program_path(command)
    if program_path:
        os.system(f'{program_path} {" ".join(args)}')
    else:
        print(f'{command}: command not found')

def main():
    while True:
        command = get_user_input()
        command_parts = command.split()
        if command_parts:
            if command_parts[0] in BUILT_IN_COMMANDS:
                execute_built_in_command(command_parts[0], command_parts[1:])
            else:
                execute_external_command(command_parts[0], command_parts[1:])

if __name__ == "__main__":
    main()
