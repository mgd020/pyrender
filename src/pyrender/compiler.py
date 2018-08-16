import re


# try:
#     import ast
# except ImportError:
#     ast = None


# some source constants
RENDER = 'render'

# the start of the compiled render function (1 space indent, start yield string)
# globals() is set to the contents of globals_ dict so the rest of the function
# can use symbols in context by name.
SOURCE_BEGIN = """\
def {render}():
 yield '""".format(render=RENDER)

# the end of the compiled render function (end string)
SOURCE_END = "'"

# tokens we replace in input string
# * set whether we are in a string or not
# * escape special characters (\n, ', \)
REPL = {
    # token: (replacement string in code, replacement string in string)
    '\n': ('\n', '\\n'),
    "'": ("'", "\\'"),
    "\\": ("\\", "\\\\"),
    # token: (replacement string, in string)
    '{{': ("'\nyield '%s'%(", False),
    '}}': (")\nyield '", True),
    '{%': ("'\n", False),
    '%}': ("\nyield '", True),
}

# used instead of indentation to know when block statements have ended
STMT_END = 'end'

# useful for removing empty statements
EMPTY_STMT = "yield ''"

# efficiently replace tokens in the string
# blackslash has to be escaped so is outside the other loop
REGEX = re.compile(r'|'.join(re.escape(k) for k in REPL.keys()))

# used to determine if the current line is a compound statement, to start block
COMPOUND_STMT = re.compile(r'^(?:if|elif|else|while|for|try|except|finally|with|def|class|async)\b')


class SubTokens(object):
    # Replace tokens with equivalent final code

    def __init__(self):
        self.in_string = True

    def __call__(self, match):
        # return string to be replaced into code (see REPL above)
        value, in_string = REPL[match.group()]
        if not isinstance(in_string, bool):
            return in_string if self.in_string else value
        self.in_string = in_string
        return value


def compile_template(string, name=None):
    """
    Compile a string into a python function that generates strings.

    Returns the function, and it's globals dict.
    """

    # source code line buffer
    lines = [SOURCE_BEGIN]

    # current indent starts at 1 as the outer function is 0
    indent = 1

    # each string token has it's own line, but code sections could have multiple so split on newline
    # will call self._repl for each token match
    for line in REGEX.sub(SubTokens(), string).split('\n'):
        line = line.strip()

        # blank
        if not line:
            continue

        # dedent
        if line == STMT_END:
            indent -= 1
            continue

        # skip empty
        if line == EMPTY_STMT:
            continue

        # add indented line
        lines.append(' ' * indent)
        lines.append(line)

        # indent
        if COMPOUND_STMT.match(line):
            lines.append(':')
            indent += 1

        # re-add newline removed by split/strip above
        lines.append('\n')

    # replace trailing newline with end source
    lines[-1] = SOURCE_END

    # make full function source
    source = ''.join(lines)

    # TODO: adjust lineno,col_offset
    # if ast:
    #     source = ast.parse(source, name)

    source = compile(source, name or '<string>', 'exec')

    locals_ = {}  # render will be defined in here
    globals_ = {}  # will be used as render's globals dict

    # exec the source to define the function
    exec(source, globals_, locals_)

    # return render function and globals dict
    return locals_[RENDER], globals_
