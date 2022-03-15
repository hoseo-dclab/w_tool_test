import sys
from classes import customException as err
from classes import find


def main():

    arg = sys.argv
    err.check_input(arg)
    
    find.find_img(arg[1], arg[2])

main()

