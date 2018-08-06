import re


class Template(object):
    """Wrap a compiled template function and add a render() method."""

    def __init__(self, func, globals_):
        self._render = func
        self._globals = globals_
        self._globals_stack = []

    def render(self, context=None):
        lines = []
        if not context:
            context = {}
        context[Compiler.APPEND] = lines.append
        self._push_context(context)
        try:
            self._render()
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


class Compiler:
    """Compile a string into a python template that can render with an optional context dict."""

    # some reused strings (makes maintenance easy)
    APPEND = '__append__'
    RENDER = 'render'

    # the start of the compiled render function (1 space indent, start string append)
    # globals() is updated with contents of context dict and append function so the
    # rest of the function can use symbols in context like they are locals
    SOURCE_BEGIN = """\
def {render}():
 {append} = globals()['{append}']
 {append}('""".format(render=RENDER, append=APPEND)

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

    def __init__(self):
        # efficiently replace tokens in the string
        # blackslash has to be escaped so is outside the other loop
        self.REGEX = re.compile(r'|'.join(k for k in self.REPL.keys() if k != '\\') + r'|\\')  # \ needs escaping

        # used to determine if the current line is a compound statement, to start block
        self.COMPOUND_STMT = re.compile(r'^(?:if|elif|else|while|for|try|except|finally|with|def|class|async)\b')

    def compile(self, string):
        # source code line buffer
        lines = [self.SOURCE_BEGIN]

        # current indent starts at 1 as the outer function is 0
        indent = 1

        # if the replacement token is in a string
        self.in_string = True

        # localise class variables for the loop
        STMT_END = self.STMT_END
        COMPOUND_STMT = self.COMPOUND_STMT
        EMPTY_STMT = self.EMPTY_STMT

        # each string token has it's own line, but code sections could have multiple so split on newline
        # will call self._repl for each token match
        for line in self.REGEX.sub(self._repl, string).split('\n'):
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
        lines[-1] = self.SOURCE_END

        # make full function source
        source = ''.join(lines)

        # compile and execute the function def, and return the template
        locals_ = {}
        globals_ = {}
        exec(source, globals_, locals_)
        return Template(locals_[self.RENDER], globals_)

    def _repl(self, match):
        # return string to be replaced into code (see REPL above)
        value, in_string = self.REPL[match.group()]
        if not isinstance(in_string, bool):
            return in_string if self.in_string else value
        self.in_string = in_string
        return value
