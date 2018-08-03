import re


class Compiler:
    """Compile a string into a python template that is callable with a context dict."""

    APPEND = '_a'
    BUFFER = '_b'
    RENDER = '_r'
    CONTEXT = '_c'
    SOURCE_BEGIN = """\
def {render}({context}=None):
 if {context}:
  globals().update({context})
 {buffer} = []
 {append} = {buffer}.append
 {append}('""".format(render=RENDER, context=CONTEXT, buffer=BUFFER, append=APPEND)
    SOURCE_END = """\
')
 return ''.join({buffer})""".format(buffer=BUFFER)
    REPL = {
        '\n': ('\n', '\\n'),
        "'": ("'", "\\'"),
        "\\": ("\\", "\\\\"),
        '{{': ("')\n{append}('%s'%(".format(append=APPEND), False),
        '}}': ("))\n{append}('".format(append=APPEND), True),
        '{%': ("')\n", False),
        '%}': ("\n{append}('".format(append=APPEND), True),
    }
    STMT_END = 'end'
    EMPTY_STMT = "%s('')" % APPEND

    def __init__(self):
        self.REGEX = re.compile(r'|'.join(k for k in self.REPL.keys() if k != '\\') + r'|\\')  # \ needs escaping
        self.COMPOUND_STMT = re.compile(r'^(?:if|elif|else|while|for|try|except|finally|with|def|class|async)\b')

    def __call__(self, string):
        lines = []
        indent = 1
        self.in_string = True
        STMT_END = self.STMT_END
        COMPOUND_STMT = self.COMPOUND_STMT
        EMPTY_STMT = self.EMPTY_STMT
        for line in self.REGEX.sub(self._repl, string).split('\n'):
            line = line.strip()
            if line == STMT_END:
                indent -= 1
                continue
            if line == EMPTY_STMT:
                continue
            lines.append(' ' * indent)
            lines.append(line)
            if COMPOUND_STMT.match(line):
                lines.append(':')
                indent += 1
            lines.append('\n')
        lines.pop(-1)  # remove trailing newline
        source = '%s%s%s' % (self.SOURCE_BEGIN, ''.join(lines), self.SOURCE_END)
        symbols = {}
        exec(source, {}, symbols)
        return symbols[self.RENDER]

    def _repl(self, match):
        value, in_string = self.REPL[match.group()]
        if not isinstance(in_string, bool):
            return in_string if self.in_string else value
        self.in_string = in_string
        return value
