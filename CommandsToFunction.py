# By TheDestruc7i0n https://thedestruc7i0n.ca
# MrGarretto for the code for traversing the command block chain https://mrgarretto.com

import mcplatform
import codecs

__version__ = "V1.4.1"

displayName = "Commands to Function"

inputs = (
    ("Converts a command block chain into a function.", "label"),
    ("The filter also includes a polyfill for conditional commands.", "label"),
    ("Select 1 repeating command block.", "label"),
    ("Ask for file save", True),
    ("If above is not checked, it will print the commands to the console.", "label"),
    ("Area effect cloud tag", ("string", "value=cond")),
    ("The above sets the tag that the area effect cloud will have, change if you have multiple functions.", "label"),
    ("Please ensure that there is a SuccessCount dummy objective in the world if you're using conditional command blocks.", "label"),
    ("Based off a filter by MrGarretto.", "label"),
    ("By TheDestruc7i0n: https://thedestruc7i0n.ca/", "label"),
)

def addPre():
    aec_summon = "summon area_effect_cloud ~ ~ ~ {Tags:[%s],Particle:\"take\"}" % tag
    scoreboard_add = "scoreboard players add @e[type=area_effect_cloud,tag=%s] SuccessCount 0" % tag
    stats_cmd = "stats entity @e[type=area_effect_cloud,tag=%s] set SuccessCount @s SuccessCount" % tag

    return [aec_summon, scoreboard_add, stats_cmd]

def perform(level, box, options):
    global tag
    tag = options["Area effect cloud tag"] or "cond"
    # the aec spawns
    pre = []
    # the amount of conditionals
    conditional_count = 0
    prefix = ""
    # the main commands
    cmds = []

    if box.volume != 1:
        raise Exception("The box must only be 1x1x1!")

    # code below is based from MrGarretto

    # since the box is 1x1x1, this is all we need
    x, y, z = box.origin

    if level.blockAt(x, y, z) == 210 or level.blockAt(x, y, z) == 137:
        doneChain = 0
        chX = x
        chY = y
        chZ = z
        whileIndex = 0
        while (doneChain == 0):
            if (level.blockAt(chX, chY, chZ) == 210 and whileIndex == 0) or (level.blockAt(chX, chY, chZ) == 137 and whileIndex == 0) or level.blockAt(chX, chY, chZ) == 211:
                bX = chX
                bY = chY
                bZ = chZ
                if level.blockDataAt(chX, chY, chZ) == 0 or level.blockDataAt(chX, chY, chZ) == 8:
                    chY -= 1
                elif level.blockDataAt(chX, chY, chZ) == 1 or level.blockDataAt(chX, chY, chZ) == 9:
                    chY += 1
                elif level.blockDataAt(chX, chY, chZ) == 2 or level.blockDataAt(chX, chY, chZ) == 10:
                    chZ -= 1
                elif level.blockDataAt(chX, chY, chZ) == 3 or level.blockDataAt(chX, chY, chZ) == 11:
                    chZ += 1
                elif level.blockDataAt(chX, chY, chZ) == 4 or level.blockDataAt(chX, chY, chZ) == 12:
                    chX -= 1
                elif level.blockDataAt(chX, chY, chZ) == 5 or level.blockDataAt(chX, chY, chZ) == 13:
                    chX += 1

                # ignore impulse command blocks from conditional checks
                if level.blockDataAt(bX, bY, bZ) > 7 and level.blockAt(chX, chY, chZ) != 137:
                    # check if there are is not an aec there, otherwise add it
                    if len(pre) < 3:
                        pre += addPre()

                    conditional_count += 1

                    prefix = ""
                    if conditional_count == 1:
                        # add init command to the last command
                        init_command = "execute @e[type=area_effect_cloud,tag=%s] ~ ~ ~ " % tag
                        cmds[-1] = init_command + cmds[-1]

                    prefix = "execute @e[type=area_effect_cloud,tag=%s,score_SuccessCount_min=1] ~ ~ ~ " % tag
                else:
                    # reset the prefix and count of conditionals if more than one
                    conditional_count = 0
                    prefix = ""

                command = level.tileEntityAt(bX, bY, bZ)["Command"].value

                # remove preceding slash if the command is non-blank
                if command:
                    if command[0] == "/":
                        command = command[1:]

                cmds.append(prefix + command)

                whileIndex += 1
            else:
                doneChain = 1

    # end code from MrGarretto

    # join the two lists together
    cmds = pre + cmds

    # convert to line by line
    commands = "\n".join(cmds)

    if options["Ask for file save"]:
        # Now save the file
        file_path = mcplatform.askSaveFile(".", "Save as...", tag, "*.mcfunction", "mcfunction")

        if file_path:
            with codecs.open(file_path, "w", "utf-8") as file:
                file.write(commands)

        # raise Exception to not save the world
        raise Exception("Saved file.\nPlease ensure that there is a SuccessCount dummy objective in the world if you're using conditional command blocks.\n\nThis is not an error.")
    else:
        print "#" * 74
        print commands
        print "#" * 74

        # raise Exception to not save the world
        raise Exception("Commands have been outputted to the console.\n\nThis is not an error.")
