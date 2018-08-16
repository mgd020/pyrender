from .compiler import compile_template


class Template(object):
    """Wrap a compiled template function and add a render() method."""

    def __init__(self, source, name=None, context=None):
        # _render is a generator of strings
        # _render_context is the globals dict for _render (id cannot change)
        self._render, self._render_context = compile_template(source, name)
        self._template_context = context
        self._context_stack = []

    def render(self, context=None):
        self._push_context(context)
        try:
            return ''.join(self._render())
        finally:
            self._pop_context()

    def _reset_context(self, context):
        # id of _render_context must not change, as _render references it internally
        self._render_context.clear()
        self._render_context['__builtins__'] = __builtins__
        if self._template_context:
            self._render_context.update(self._template_context)
        if context:
            self._render_context.update(context)

    def _push_context(self, context):
        # push a shallow copy of current context onto the stack
        self._context_stack.append(dict(self._render_context))
        self._reset_context(context)

    def _pop_context(self):
        self._reset_context(self._context_stack.pop())
