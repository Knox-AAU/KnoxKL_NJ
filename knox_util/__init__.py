import asyncio
import sys
import builtins as __builtins__
from inspect import getframeinfo, stack


parserArgs = None

def get_file_debug_info(stack_frm: int) -> str:
    """
    Input:
        stack_frm: int - An integer representing the stackframe to capture

    This method will get debug information for a verbose print statement
    """
    try:
        caller = getframeinfo(stack()[stack_frm][0])
    except:
        caller = getframeinfo(stack()[stack_frm-1][0])
    return f'{caller.filename.replace(sys.path[0]+"/","")}:{caller.lineno} '

def print(message: str, level: str = 'info') -> None:
    """
    Input:
        message: str - The message to print to the user
        level: str - The verbosity level to display to the user. This is used to calculate wether the message is shown
    
    This method overrides the default print method, allowing for more detailed prints.
    In order to make prints more detailed, the level must be specified. This will label prints
    
    Levels:
        off - default print
        error - Prints a red error message
        warning - Prints a yellow warning message
        info - Prints a white info message
        debug - Prints a blue debug message
        default - info
    """
    if level == 'off':
        __builtins__.print(message)
        return
    if parserArgs.verb != 'off' and parserArgs.verb != 'quiet':
        label_switcher = {
            1: '\033[1;4;31m[ERROR]\033[0;31m',
            2: '\033[1;4;33m[WARNING]\033[0;33m',
            3: '\033[1;4;37m[INFO]\033[0;37m',
            4: '\033[1;4;34m[DEBUG]\033[0;34m'
        }
        level_switcher = {
            'error': 1,
            'warning': 2,
            'info': 3,
            'debug': 4,
            'info-only': 5
        }
        log_level = level_switcher.get(parserArgs.verb, 3)
        specified_log_level = level_switcher.get(level, 0)
        file_debug_info = ''
        if specified_log_level == 0:
            file_debug_info = get_file_debug_info(3)
            __builtins__.print(f'{label_switcher[2]} {file_debug_info}Invalid log level specified <{level}>. Defaulting to Info\033[0m')
            specified_log_level = 3
            file_debug_info = ''
        if log_level == 5 and (specified_log_level == 3 or specified_log_level == 5):
            __builtins__.print(f'{label_switcher[3]} {message}\033[0m')
            return

        if specified_log_level <= 2:
            file_debug_info = get_file_debug_info(2)
        elif specified_log_level == 4:
            file_debug_info = get_file_debug_info(3)
            
        if specified_log_level <= log_level and log_level != 5:
            __builtins__.print(f'{label_switcher[specified_log_level]} {file_debug_info}{message}\033[0m')
    else:
        pass

def background_process(func):
    """
    Returns:
        Event loop

    Annotation to run function in background using asyncio
    """
    def wrapped(*args, **kwargs):
        """
        Returns:
            Event loop

        Wrapped function for asyncronous running of functions
        """
        print('Starting background process...', 'warning')
        return asyncio.get_event_loop().run_in_executor(None, func, *args, **kwargs)
    return wrapped