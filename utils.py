import colorama

def err(text, _exit=False):
    print(f'\n{colorama.Fore.RED}(!) {text}{colorama.Style.RESET_ALL}')
    if _exit:
        exit(1)

def print_intro():
    print(f'{colorama.Back.YELLOW}MALATÌA <github.com/gcrbr>{colorama.Style.RESET_ALL}')