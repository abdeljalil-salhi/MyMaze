# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/05 20:10:28 by absalhi           #+#    #+#              #
#    Updated: 2022/12/05 22:24:40 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":
    from srcs.utilities import clear, printf, BLUE, RED

    clear()
    printf("Loading...\n", BLUE)

    from srcs.mymaze import MyMaze

    try: MyMaze()
    except KeyboardInterrupt: printf("\nExiting...\n", RED)
    