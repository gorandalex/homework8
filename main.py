from models import Author, Quote
import connect
import commands

COMMANDS = {
    'help': commands.show_help,
    'name': commands.find_by_name,
    'tag': commands.find_by_tags,
    'exit': commands.show_exit
}

TYPE_MESSAGE = {
    'SMS': 'sms',
    'EMAIL': 'email'
}


def get_answer_function(answer):
    return COMMANDS.get(answer, commands.command_error)


def run_command(user_command):
    command = user_command
    params = ''
    for key in COMMANDS:
        if user_command.lower().startswith(key + ':'):
            command = key
            params = user_command[len(command) + 1:]
            break
    if params:
        return get_answer_function(command)(params.strip())
    else:
        return get_answer_function(command)()


def search_informations():
    while True:
        command_user = input("Введіть вашу команду: ")
        answer = run_command(command_user.strip())
        print(answer)
        if answer == 'Good bye!':
            break


if __name__ == '__main__':
    search_informations()
