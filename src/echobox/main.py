#!/usr/bin/env python
""" echobox - write arguments in a box to the standard output
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import os
import platform
import shutil
import sys

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: echobox - write arguments in a box to the standard output v1.2.1 (September 26, 2021) by Hubert Tournier $"

# Cf. https://en.wikipedia.org/wiki/Box-drawing_character
# Cf. https://unicode-table.com/fr/#box-drawing
STYLES = {
    "basic": {
        "Upper left corner": "#",
        "Horizontal line": "#",
        "Upper right corner": "#",
        "Vertical line": "#",
        "Lower left corner": "#",
        "Lower right corner": "#",
    },
    "ascii": {
        "Upper left corner": "+",
        "Horizontal line": "-",
        "Upper right corner": "+",
        "Vertical line": "|",
        "Lower left corner": "+",
        "Lower right corner": "+",
    },
    "single": {
        "Upper left corner": "\u250c",
        "Horizontal line": "\u2500",
        "Upper right corner": "\u2510",
        "Vertical line": "\u2502",
        "Lower left corner": "\u2514",
        "Lower right corner": "\u2518",
    },
    "double": {
        "Upper left corner": "\u2554",
        "Horizontal line": "\u2550",
        "Upper right corner": "\u2557",
        "Vertical line": "\u2551",
        "Lower left corner": "\u255a",
        "Lower right corner": "\u255d",
    },
    "block": {
        "Upper left corner": "\u2588",
        "Horizontal line": "\u2588",
        "Upper right corner": "\u2588",
        "Vertical line": "\u2588",
        "Lower left corner": "\u2588",
        "Lower right corner": "\u2588",
    },
}
if platform.system() != "Windows":
    STYLES["hatched"] = {
        "Upper left corner": "\u250f",
        "Horizontal line": "\u2501",
        "Upper right corner": "\u2513",
        "Vertical line": "\u2503",
        "Lower left corner": "\u2517",
        "Lower right corner": "\u251b",
    }
    STYLES["curved"] = {
        "Upper left corner": "\u256d",
        "Horizontal line": "\u2500",
        "Upper right corner": "\u256e",
        "Vertical line": "\u2502",
        "Lower left corner": "\u2570",
        "Lower right corner": "\u256f",
    }

# default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Style": "basic",
    "Columns": shutil.get_terminal_size()[0],
    "Alignment": "left",
    "Leading lines": 0,
    "Basic char": "#",
    "Fill char": " ",
    "Surrounding spaces": 3,
    "Internal lines": 1,
    "Trailing lines": 1,
}


################################################################################
def initialize_debugging(program_name):
    """Debugging set up"""
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)


################################################################################
def display_help():
    """Displays usage and help"""
    print(
        "usage: echobox [-a|--align name] [-b|--basic-char char] [-d|--debug]",
        file=sys.stderr,
    )
    print(
        "       [-f|--fill-char char] [-h|--help|-?] [-i|--inter-lines number]",
        file=sys.stderr,
    )
    print(
        "       [-l|--lead-lines number] [-S|--style name] [-s|--spaces number]",
        file=sys.stderr,
    )
    print(
        "       [-t|--trail-lines number] [-v|--version] [--] [string ...]",
        file=sys.stderr
    )
    print(
        "  ----------------   ---------------------------------------------------",
        file=sys.stderr,
    )
    print(
        "  -a|--align         Box alignment (left, middle, center, right): %s"
        % parameters["Alignment"],
        file=sys.stderr,
    )
    print(
        "  -b|--basic-char    Character to use for basic style: '%s'"
        % parameters["Basic char"],
        file=sys.stderr,
    )
    print(
        "  -f|--fill-char     Character to use to fill background: '%s'"
        % parameters["Fill char"],
        file=sys.stderr,
    )
    print(
        "  -i|--inter-lines   Blank lines around the text: %d"
        % parameters["Internal lines"],
        file=sys.stderr,
    )
    print(
        "  -l|--lead-lines    Blank lines before the box: %d"
        % parameters["Leading lines"],
        file=sys.stderr,
    )
    print(
        "  -S|--style         Style to use: %s" % parameters["Style"], file=sys.stderr
    )
    print(
        "  -s|--spaces        Spaces around the text: %d"
        % parameters["Surrounding spaces"],
        file=sys.stderr,
    )
    print(
        "  -t|--trail-lines   Blank lines after the box: %d"
        % parameters["Trailing lines"],
        file=sys.stderr,
    )
    print("  --debug            Enable debug mode", file=sys.stderr)
    print(
        "  --help|-?          Print usage and this help message and exit",
        file=sys.stderr,
    )
    print("  --version          Print version and exit", file=sys.stderr)
    print("  --                 Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)
    print("Available styles: " + " ".join(STYLES.keys()), file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def process_environment_variables():
    """Process environment variables"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    if "ECHOBOX_STYLE" in os.environ.keys():
        if os.environ["ECHOBOX_STYLE"] in STYLES.keys():
            parameters["Style"] = os.environ["ECHOBOX_STYLE"]
        else:
            logging.error("Unknown style in the ECHOBOX_STYLE environment variable")
            parameters["Style"] = "basic"

    if "ECHOBOX_ALIGN" in os.environ.keys():
        if os.environ["ECHOBOX_ALIGN"].lower() in ("center", "middle"):
            parameters["Alignment"] = "center"
        elif os.environ["ECHOBOX_ALIGN"].lower() == "left":
            parameters["Alignment"] = "left"
        elif os.environ["ECHOBOX_ALIGN"].lower() == "right":
            parameters["Alignment"] = "right"
        else:
            logging.error("Unknown alignment in the ECHOBOX_ALIGN environment variable")
            parameters["Alignment"] = "left"

    if (
        "ECHOBOX_BASIC_CHAR" in os.environ.keys()
        and len(os.environ["ECHOBOX_BASIC_CHAR"]) == 1
    ):
        parameters["Basic char"] = os.environ["ECHOBOX_BASIC_CHAR"]
        STYLES["basic"]["Upper left corner"] = parameters["Basic char"]
        STYLES["basic"]["Horizontal line"] = parameters["Basic char"]
        STYLES["basic"]["Upper right corner"] = parameters["Basic char"]
        STYLES["basic"]["Vertical line"] = parameters["Basic char"]
        STYLES["basic"]["Lower left corner"] = parameters["Basic char"]
        STYLES["basic"]["Lower right corner"] = parameters["Basic char"]

    if (
        "ECHOBOX_FILL_CHAR" in os.environ.keys()
        and len(os.environ["ECHOBOX_FILL_CHAR"]) == 1
    ):
        parameters["Fill char"] = os.environ["ECHOBOX_FILL_CHAR"]

    if "ECHOBOX_SPACES" in os.environ.keys():
        if os.environ["ECHOBOX_SPACES"].isdigit():
            parameters["Surrounding spaces"] = int(os.environ["ECHOBOX_SPACES"])
        else:
            logging.error(
                "Non numeric value in the ECHOBOX_SPACES environment variable"
            )

    if "ECHOBOX_INTER_LINES" in os.environ.keys():
        if os.environ["ECHOBOX_INTER_LINES"].isdigit():
            parameters["Internal lines"] = int(os.environ["ECHOBOX_INTER_LINES"])
        else:
            logging.error(
                "Non numeric value in the ECHOBOX_INTER_LINES environment variable"
            )

    if "ECHOBOX_LEAD_LINES" in os.environ.keys():
        if (
            os.environ["ECHOBOX_LEAD_LINES"].isdigit()
            and os.environ["ECHOBOX_LEAD_LINES"] >= 0
        ):
            parameters["Leading lines"] = int(os.environ["ECHOBOX_LEAD_LINES"])
        else:
            logging.error(
                "Non numeric value in the ECHOBOX_LEAD_LINES environment variable"
            )

    if "ECHOBOX_TRAIL_LINES" in os.environ.keys():
        if (
            os.environ["ECHOBOX_TRAIL_LINES"].isdigit()
            and os.environ["ECHOBOX_TRAIL_LINES"] >= 0
        ):
            parameters["Trailing lines"] = int(os.environ["ECHOBOX_TRAIL_LINES"])
        else:
            logging.error(
                "Non numeric value in the ECHOBOX_TRAIL_LINES environment variable"
            )

    if "ECHOBOX_DEBUG" in os.environ.keys():
        logging.disable(logging.NOTSET)

    # The following environment variable is provided by the Bash shell and some others,
    # but not necessarily exported:
    if "COLUMNS" in os.environ.keys() and os.environ["COLUMNS"].isdigit():
        parameters["Columns"] = int(os.environ["COLUMNS"])

    # The following will only work if you have set ECHOBOX_DEBUG:
    logging.debug("process_environment_variables(): parameters:")
    logging.debug(parameters)


################################################################################
def process_command_line():
    """Process command line"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "a:b:df:hi:l:S:s:t:v?"
    string_options = [
        "align=",
        "basic-char=",
        "debug",
        "fill-char=",
        "help",
        "inter-lines=",
        "lead-lines=",
        "style=",
        "spaces=",
        "trail-lines=",
        "version",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        display_help()
        sys.exit(1)

    for option, argument in options:

        if option in ("-a", "--align"):
            if argument.lower() in ("left", "center", "middle", "right"):
                parameters["Alignment"] = argument.lower()
            else:
                logging.critical(
                    "-a/--align parameter must be one of: left, middle, center, right"
                )
                sys.exit(1)

        elif option in ("-b", "--basic-char"):
            if len(argument) == 1:
                parameters["Basic char"] = argument
                STYLES["basic"]["Upper left corner"] = parameters["Basic char"]
                STYLES["basic"]["Horizontal line"] = parameters["Basic char"]
                STYLES["basic"]["Upper right corner"] = parameters["Basic char"]
                STYLES["basic"]["Vertical line"] = parameters["Basic char"]
                STYLES["basic"]["Lower left corner"] = parameters["Basic char"]
                STYLES["basic"]["Lower right corner"] = parameters["Basic char"]
            else:
                logging.critical("-b/--basic-char parameter must be a single character")
                sys.exit(1)

        elif option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("-f", "--fill-char"):
            if len(argument) == 1:
                parameters["Fill char"] = argument
            else:
                logging.critical("-f/--fill-char parameter must be a single character")
                sys.exit(1)

        elif option in ("--help", "-?"):
            display_help()
            sys.exit(0)

        elif option in ("-i", "--inter-lines"):
            if argument.isdigit() and int(argument) >= 0:
                parameters["Internal lines"] = int(argument)
            else:
                logging.critical(
                    "-i/--inter-lines parameter must be a positive integer"
                )
                sys.exit(1)

        elif option in ("-l", "--lead-lines"):
            if argument.isdigit() and int(argument) >= 0:
                parameters["Leading lines"] = int(argument)
            else:
                logging.critical("-l/--lead-lines parameter must be a positive integer")
                sys.exit(1)

        elif option in ("-S", "--style"):
            if argument.lower() in STYLES.keys():
                parameters["Style"] = argument.lower()
            else:
                logging.critical(
                    "-S/--style parameter must be one of: %s", " ".join(STYLES.keys())
                )
                sys.exit(1)

        elif option in ("-s", "--spaces"):
            if argument.isdigit() and int(argument) >= 0:
                parameters["Surrounding spaces"] = int(argument)
            else:
                logging.critical("-s/--spaces parameter must be a positive integer")
                sys.exit(1)

        elif option in ("-t", "--trail-lines"):
            if argument.isdigit() and int(argument) >= 0:
                parameters["Trailing lines"] = int(argument)
            else:
                logging.critical(
                    "-t/--trail-lines parameter must be a positive integer"
                )
                sys.exit(1)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def print_indentation(nb_spaces):
    """Prints indentation spaces"""
    for _ in range(nb_spaces):
        print(" ", end="")


################################################################################
def print_upper_box_line(text_indent, text_width_with_spaces):
    """Prints the upper box line"""
    print_indentation(text_indent)
    print(STYLES[parameters["Style"]]["Upper left corner"], end="")
    for _ in range(text_width_with_spaces):
        print(STYLES[parameters["Style"]]["Horizontal line"], end="")
    print(STYLES[parameters["Style"]]["Upper right corner"])


################################################################################
def print_inter_lines(text_indent, text_width_with_spaces):
    """Prints inner box lines if requested"""
    for _ in range(parameters["Internal lines"]):
        print_indentation(text_indent)
        print(STYLES[parameters["Style"]]["Vertical line"], end="")
        for _ in range(text_width_with_spaces):
            print(parameters["Fill char"], end="")
        print(STYLES[parameters["Style"]]["Vertical line"])


################################################################################
def print_text_line(text_indent, line, longuest_line):
    """Prints the text in an inner box line"""
    print_indentation(text_indent)
    print(STYLES[parameters["Style"]]["Vertical line"], end="")
    for _ in range(parameters["Surrounding spaces"]):
        print(parameters["Fill char"], end="")
    if len(line) < longuest_line:
        for _ in range((longuest_line - len(line)) // 2):
            print(parameters["Fill char"], end="")
    print(line, end="")
    if len(line) < longuest_line:
        for _ in range(((longuest_line - len(line)) // 2) + (longuest_line - len(line)) % 2):
            print(parameters["Fill char"], end="")
    for _ in range(parameters["Surrounding spaces"]):
        print(parameters["Fill char"], end="")
    print(STYLES[parameters["Style"]]["Vertical line"])


################################################################################
def print_lower_box_line(text_indent, text_width_with_spaces):
    """Prints the lower box line"""
    print_indentation(text_indent)
    print(STYLES[parameters["Style"]]["Lower left corner"], end="")
    for _ in range(text_width_with_spaces):
        print(STYLES[parameters["Style"]]["Horizontal line"], end="")
    print(STYLES[parameters["Style"]]["Lower right corner"])


################################################################################
def print_blank_lines(nb_lines):
    """Prints blank lines if requested"""
    for _ in range(nb_lines):
        print()


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])

    initialize_debugging(program_name)
    process_environment_variables()
    arguments = process_command_line()

    # Reading from standard input if there are no arguments:
    text = []
    longuest_line = 0
    if len(arguments):
        arguments_line = " ".join(arguments)
        text = arguments_line.split("\\n")
        for line in text:
            if len(line) > longuest_line:
                longuest_line = len(line)
    else:
        for line in sys.stdin:
            line = line.strip()
            text.append(line)
            if len(line) > longuest_line:
                longuest_line = len(line)

    text_width_with_spaces = longuest_line + 2 * parameters["Surrounding spaces"]
    text_width_with_spaces_and_borders = text_width_with_spaces + 2
    if parameters["Alignment"] == "left":
        text_indent = 0
    elif parameters["Alignment"] == "right":
        text_indent = parameters["Columns"] - text_width_with_spaces_and_borders
    else:
        text_indent = (parameters["Columns"] - text_width_with_spaces_and_borders) // 2
    if text_indent < 0:
        text_indent = 0

    print_blank_lines(parameters["Leading lines"])
    print_upper_box_line(text_indent, text_width_with_spaces)
    print_inter_lines(text_indent, text_width_with_spaces)
    for line in text:
        print_text_line(text_indent, line, longuest_line)
    print_inter_lines(text_indent, text_width_with_spaces)
    print_lower_box_line(text_indent, text_width_with_spaces)
    print_blank_lines(parameters["Trailing lines"])

    sys.exit(0)


if __name__ == "__main__":
    main()
