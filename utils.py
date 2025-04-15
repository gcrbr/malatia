import colorama
import os
import glob

def err(text, _exit=False):
    print(f'\n{colorama.Fore.RED}(!) {text}{colorama.Style.RESET_ALL}')
    if _exit:   exit(1)

def print_intro():
    print(f'{colorama.Back.YELLOW}MALATÌA <github.com/gcrbr>{colorama.Style.RESET_ALL}')

def get_source_files(path):
    return [os.path.basename(f)[:-3] for f in glob.glob(path.replace('.', '/') + '/*.py')]