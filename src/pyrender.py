import re


class Compiler:
    """Compile a string into a python template that is callable with a context dict."""

    # some reused strings (makes maintenance easy)
    APPEND = '_a'
    BUFFER = '_b'
    RENDER = '_r'
    CONTEXT = '_c'

    # the start of the compiled render function (1 space indent, start string append)
    # once the function gets context (a dict), it updates globals() so the rest of the function
    # can use symbols in context like they are locals (this doesn't seem to affect outer contexts)
    SOURCE_BEGIN = """\
def {render}({context}=None):
 if {context}:
  globals().update({context})
 {buffer} = []
 {append} = {buffer}.append
 {append}('""".format(render=RENDER, context=CONTEXT, buffer=BUFFER, append=APPEND)

    # the end of the compiled render function (1 space indent, end string append)
    SOURCE_END = """\
')
 return ''.join({buffer})""".format(buffer=BUFFER)

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
    EMPTY_STMT = "%s('')" % APPEND

    def __init__(self):
        # efficiently replace tokens in the string
        # blackslash has to be escaped so is outside the other loop
        self.REGEX = re.compile(r'|'.join(k for k in self.REPL.keys() if k != '\\') + r'|\\')  # \ needs escaping

        # used to determine if the current line is a compound statement, to start block
        self.COMPOUND_STMT = re.compile(r'^(?:if|elif|else|while|for|try|except|finally|with|def|class|async)\b')

    def __call__(self, string):
        # source code line buffer
        lines = []

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

        # remove trailing newline
        lines.pop(-1)

        # make full function source
        source = '%s%s%s' % (self.SOURCE_BEGIN, ''.join(lines), self.SOURCE_END)

        # compile and execute the function def, and return the new render function
        symbols = {}
        exec(source, {}, symbols)
        return symbols[self.RENDER]

    def _repl(self, match):
        # return string to be replaced into code (see REPL above)
        value, in_string = self.REPL[match.group()]
        if not isinstance(in_string, bool):
            return in_string if self.in_string else value
        self.in_string = in_string
        return value
