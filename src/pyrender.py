import re


class Template:
    SOURCE_BEGIN = "__render__('"
    SOURCE_END = "')"
    REPL = {
        # TODO: escale "'", "\n"
        '\n': ('\\n', None),
        '{{': ("')\n__render__(str(", True),
        '}}': ("))\n__render__('", False),
        '{%': ("')\n", True),
        '%}': ("\n__render__('", False),
    }
    REGEX = re.compile(r'|'.join(REPL.keys()))
    COMPOUND_STMT = re.compile(r'^(?:if|elif|else|while|for|try|except|finally|with|def|class|async)\b')
    STMT_END = 'end'
    EMPTY_STMT = "__render__('')"

    def __init__(self, string):
        lines = []
        indent = 0
        self.strip_newlines = False
        STMT_END = self.STMT_END
        COMPOUND_STMT = self.COMPOUND_STMT
        EMPTY_STMT = self.EMPTY_STMT
        PASS_STMT = 'pass'
        for line in self.REGEX.sub(self._repl, string).split('\n'):
            line = line.strip()
            if line == STMT_END:
                indent -= 1
                continue
            if line == EMPTY_STMT:
                line = PASS_STMT
            lines.append(' ' * indent)
            lines.append(line)
            if COMPOUND_STMT.match(line):
                lines.append(':')
                indent += 1
            lines.append('\n')
        lines.pop(-1)  # remove trailing newline
        source = '%s%s%s' % (self.SOURCE_BEGIN, ''.join(lines), self.SOURCE_END)
        self.code = compile(source, '<string>', 'exec')

    def _repl(self, match):
        value, strip_newlines = self.REPL[match.group()]
        if strip_newlines is None:
            return '' if self.strip_newlines else value
        self.strip_newlines = strip_newlines
        return value

    def render(self, context=None):
        text = []
        if not context:
            context = {}
        context['__render__'] = text.append
        exec(self.code, context)
        return ''.join(text)
