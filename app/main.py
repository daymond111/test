import sys

def prompt_user():
    sys.stdout.write("$ ")
    sys.stdout.flush()
    return input()

def execute_command(command):
    match command:
        case "exit 0":
            sys.exit(0)
        case command if command.startswith("echo "):
            print(command[5:])
        case _:
            print(f"{command}: command not found")

def main():
    while True:
        command = prompt_user()
        execute_command(command)

if __name__ == "__main__":
    main()
