import re


# some source constants
APPEND = '__append__'
RENDER = 'render'

# the start of the compiled render function (1 space indent, start string append)
# globals() is set to the contents of globals_ dict so the rest of the function
# can use symbols in context by name. localise append for speed.
SOURCE_BEGIN = """\
def {render}({append}):
 {append}('""".format(append=APPEND, render=RENDER)

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

    def __init__(self, func, globals_):
        self._render = func
        self._globals = globals_
        self._globals_stack = []

    def render(self, context=None):
        lines = []
        self._push_context(context or {})
        try:
            self._render(lines.append)
        except:
            raise
        else:
            return ''.join(lines)
        finally:
            self._pop_context()

    def _reset_context(self, context):
        # id of globlas must not change
        self._globals.clear()
        self._globals['__builtins__'] = __builtins__
        self._globals.update(context)

    def _push_context(self, context):
        # push a shallow copy of current globals onto the stack
        self._globals_stack.append(dict(self._globals))
        self._reset_context(context)

    def _pop_context(self):
        self._reset_context(self._globals_stack.pop())


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

    # compile the source, and return the template
    locals_ = {}  # to extract function def
    globals_ = {}  # to put context in
    exec(source, globals_, locals_)
    return Template(locals_[RENDER], globals_)
