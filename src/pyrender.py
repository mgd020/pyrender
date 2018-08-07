import re


# the name of the write method in the template
APPEND = '__append__'

# the start of the compiled render function (1 space indent, start string append)
# globals() is updated with contents of context dict and append function so the
# rest of the function can use symbols in context like they are locals
SOURCE_BEGIN = "{append}('".format(append=APPEND)

# the end of the compiled render function (1 space indent, end string append)
SOURCE_END = "')"

# tokens we replace in input string
# * set whether we are in a string or not
# * escape special characters (\n, ', \)
REPL = {
    # token: (replacement string in code, replacement string in string)
    '\n': ('\n', '\\n'),
    "'": ("'", "\\'"),
    "\\": ("\\", "\\\\"),
    # token: (replacement string, in string)
    '{{': ("')\n{append}('%s'%(".format(append=APPEND), False),
    '}}': ("))\n{append}('".format(append=APPEND), True),
    '{%': ("')\n", False),
    '%}': ("\n{append}('".format(append=APPEND), True),
}

# used instead of indentation to know when block statements have ended
STMT_END = 'end'

# useful for removing empty statements
EMPTY_STMT = "{append}('')".format(append=APPEND)

# efficiently replace tokens in the string
# blackslash has to be escaped so is outside the other loop
REGEX = re.compile(r'|'.join(k for k in REPL.keys() if k != '\\') + r'|\\')  # \ needs escaping

# used to determine if the current line is a compound statement, to start block
COMPOUND_STMT = re.compile(r'^(?:if|elif|else|while|for|try|except|finally|with|def|class|async)\b')


class Template(object):
    """Wrap a compiled template function and add a render() method."""

    def __init__(self, code):
        self.code = code

    def render(self, context=None):
        lines = []
        locals_ = {
            APPEND: lines.append,
        }
        if context:
            locals_.update(context)
        exec(self.code, {}, locals_)
        return ''.join(lines)


class SubTokens(object):
    def __init__(self):
        self.in_string = True

    def __call__(self, match):
        # return string to be replaced into code (see REPL above)
        value, in_string = REPL[match.group()]
        if not isinstance(in_string, bool):
            return in_string if self.in_string else value
        self.in_string = in_string
        return value


def compile_template(string):
    """Compile a string into a python template that can render with an optional context dict."""

    # source code line buffer
    lines = [SOURCE_BEGIN]

    # current indent starts at 1 as the outer function is 0
    indent = 0

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

    # compile the source, and return the template
    code = compile(source, '<string>', 'exec')
    return Template(code)
