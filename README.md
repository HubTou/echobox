# Installation
pip install [pnu-echobox](https://pypi.org/project/pnu-echobox/)

# ECHOBOX(1)

## NAME
echobox - write arguments in a box to the standard output

## SYNOPSIS
**echobox**
[-a\|--align name]
[-b\|--basic-char char]
[-f\|--fill-char char]
[-i\|--inter-lines number]
[-l\|--lead-lines number]
[-S\|--style name]
[-s\|--spaces number]
[-t\|--trail-lines number]
[--debug]
[--help\|-?]
[--version]
[--]
[string ...]

## DESCRIPTION
The **echobox** utility writes any specified operands, separated by single blank (' ') characters, in a box, to the standard output.
The "\n" substring is used to split the concatenated operands into multiple lines.

If there are no arguments provided on the command line, standard input is read
(until a Control-D (Unix) or Control-Z (Windows) character is sent).

### OPTIONS
Options | Use
------- | ---
-a\|--align name|Sets the alignment to use. Possible values: left (default), center, middle, right.
-b\|--basic-char char|Sets the character to use with the basic style. Default value: '#'.
-f\|--fill-char char|Sets the character to use to fill the box. Default value: ' '.
-i\|--inter-lines number|Sets the number of lines separating the text from the box on the top and bottom sides. Default value: 1.
-l\|--lead-lines number|Sets the number of blank lines preceding the box. Default value: 0.
-S\|--style name|Sets the style to use. Possible values: basic (default), ascii, single, curved, hatched, double, block.
-s\|--spaces number|Sets the number of spaces separating the text from the box on the left and right sides. Default value: 3.
-t\|--trail-lines number|Sets the number of blank lines following the box. Default value: 1.
--debug|Enable debug level messages.
--help\|-?|Print usage and a short help message and exit.
--version|Print version and exit.
--|Options processing terminator. Contrarily to the [echo(1)](https://www.freebsd.org/cgi/man.cgi?query=echo) command, it is recognized as such.

## ENVIRONMENT
Environment variables are processed first and thus overridden by command line options.

Variable | Use
-------- | ---
ECHOBOX_STYLE | Sets the style to use.
ECHOBOX_ALIGN | Sets the alignment to use.
ECHOBOX_BASIC_CHAR | Sets the character to use with the basic style.
ECHOBOX_FILL_CHAR | Sets the character to use to fill the box.
ECHOBOX_SPACES | Sets the number of spaces separating the text from the box on the left and right sides.
ECHOBOX_INTER_LINES | Sets the number of lines separating the text from the box on the top and bottom sides.
ECHOBOX_LEAD_LINES | Sets the number of blank lines preceding the box.
ECHOBOX_TRAIL_LINES | Sets the number of blank lines following the box.
ECHOBOX_DEBUG | Enable debug level messages.
COLUMNS | Defines the number of columns in the terminal window. This variable is sometimes provided by the [Bash](http://www.gnu.org/software/bash/) shell and some others, but not necessarily exported. It's used for center and right alignments. Default value: 80.

## EXIT STATUS
The **echobox** utility exits 0 on success, and >0 if an error occurs.

## SEE ALSO
[dialog(1)](https://www.freebsd.org/cgi/man.cgi?query=dialog),
[fortune(6)](https://github.com/HubTou/fortune/blob/main/README.md)

https://en.wikipedia.org/wiki/Box-drawing_character

https://unicode-table.com/fr/#box-drawing

## STANDARDS
The **echobox** command is not a standard [UNIX](https://en.wikipedia.org/wiki/Unix)/[POSIX](https://en.wikipedia.org/wiki/POSIX) command.

It tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## PORTABILITY
Tested OK under Windows, though some of the styles are not available
(the [hatched and curved Unicode characters](https://unicode-table.com/fr/#box-drawing) are not fully recognized in the cmd.exe and PowerShell command prompts).

## HISTORY
The **echobox** command was created as an example for the [PNU project](https://github.com/HubTou/PNU),
demonstrating how to process the environment and the command line, and use the [Python logging module](https://docs.python.org/3/library/logging.html).

It's also used as a filter for [fortune(6)](https://github.com/HubTou/fortune/blob/main/README.md) output,
in order to introduce some [boxology](http://www.catb.org/jargon/html/B/boxology.html).

## LICENSE
This utility is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

## CAVEATS
Specifying basic or fill [Unicode](https://home.unicode.org/) characters is not currently possible with the environment and command line options.

Display will overflow if your text is wider than your console.

