import sys
import os

BUILT_IN_COMMANDS = ['echo', 'exit', 'type']

def prompt_user():
    sys.stdout.write("$ ")
    sys.stdout.flush()
    return input()

def execute_command(command):
    cmd = command[5:]
    PATHS = os.environ.get("PATH").split(os.pathsep)
    command_path = None

    match command:
        case "exit 0":
            sys.exit(0)
        case command if command.startswith("echo "):
            print(cmd)
        case command if command.startswith("type "):
            for path in PATHS:
                if os.path.isfile(os.path.join(path, cmd)):
                    command_path = os.path.join(path, cmd)
                    break
            if cmd in BUILT_IN_COMMANDS:
                print(f"{cmd} is a shell builtin")
            elif command_path:
                print(f"{cmd} is {command_path}")
            else:
                print(f"{cmd}: not found")
        case _:
            print(f"{command}: command not found")

def main():
    while True:
        command = prompt_user()
        execute_command(command)

if __name__ == "__main__":
    main()
