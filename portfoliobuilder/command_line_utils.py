
def has_num_args(command, num_args):
    '''
    Note: Pass entire command to this function, not just arguments.
    Return True if command has exactly num_args arguments, False otherwise.
    '''
    split_command = command.split(' ')
    if len(split_command) == (num_args + 1):
        return True
    print('Invalid command. Incorrect number of arguments.')
    return False