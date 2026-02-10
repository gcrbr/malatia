from os import stat
import colorama
import os
import glob

class Console:
    @staticmethod
    def print_intro():
        print(f'{colorama.Back.YELLOW}MALATÌA – low cost journey searcher{colorama.Style.RESET_ALL}')
    
    @staticmethod
    def info(text: str):
        print(f'{colorama.Fore.CYAN}@ {text}{colorama.Style.RESET_ALL}')

    @staticmethod
    def warning(text: str):
        print(f'{colorama.Fore.YELLOW}⚠ {text}{colorama.Style.RESET_ALL}')

    @staticmethod
    def err(text: str, _exit: bool=False):
        print(f'\n{colorama.Fore.RED}✖ {text}{colorama.Style.RESET_ALL}')
        if _exit:   exit(1)
    
    @staticmethod
    def empty_line():
        print('')

class Files:
    @staticmethod
    def get_source_files(path):
        return [os.path.basename(f)[:-3] for f in glob.glob(path.replace('.', '/') + '/*.py')]