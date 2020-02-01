MAP_WIDTH = MAP_HEIGHT = 8

LEVEL = """\
####### #########
#               #
# ##### ####### #
# #   # #       #
# ### # # #######
#   #   #       #
# # ########### #
# #   #     #   #
# ### # ### # ###
#   #   #   #   #
####### # #######
# #     #       #
# # ########### #
#   #           #
# ### ######### #
#   #     #     #
######### #######\
""".split("\n")

# convert into walls
X_WALLS = [
    [LEVEL[2*y+1][2*x]=='#' for x in range(9)] for y in range(8)
]

Y_WALLS = [
    [LEVEL[2*y][2*x+1] == '#' for x in range(8)] for y in range(9)
]

# WORLD = dict(
#     MAP=LEVEL,
#     X_WALLS=X_WALLS,
#     Y_WALLS=Y_WALLS
# )

if __name__ == '__main__':
    print(X_WALLS)
    print(Y_WALLS)
