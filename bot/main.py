# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/07 14:59:03 by absalhi           #+#    #+#              #
#    Updated: 2022/12/07 15:13:23 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":
    
    from srcs.utilities import clear, printf, BLUE, RED

    clear()
    printf("Loading...\n", BLUE)

    from srcs.mymazebot import MyMazeBot

    try: MyMazeBot()
    except KeyboardInterrupt: printf("\nExiting...\n", RED)