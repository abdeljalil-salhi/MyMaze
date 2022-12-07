# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utilities.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/05 22:07:19 by absalhi           #+#    #+#              #
#    Updated: 2022/12/05 22:20:59 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from os import system, get_terminal_size, name
from sys import stdout


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def colorable(stream):
    
    if not (hasattr(stream, "isatty") and stream.isatty): return False
    try:
        from curses import setupterm, tigetnum
        setupterm()
        return tigetnum("colors") > 2
    except: return False


def printf(text, colour=WHITE):
    
    stdout.write("\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m") if colorable else stdout.write(text)


def clear():
    
    system("cls") if name == "nt" else system("clear")


def sep():

    try: (w, _) = get_terminal_size()
    except: w = 25
    printf("-" * w + "\n", GREEN)
