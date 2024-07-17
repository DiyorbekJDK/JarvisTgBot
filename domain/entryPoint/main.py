from pathlib import Path
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from domain.mainCode.allCode import allCode
from domain.functions.dbFunctions.databaseFunctions import *


##############################
# Entry point of python code #
##############################

def main():
    print("Bot is working...")
    allCode()


if __name__ == '__main__':
    main()
