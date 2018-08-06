# Copyright 2016 The Spitfire Authors. All Rights Reserved.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import print_function

import copy
import optparse
import string
try:
    from StringIO import StringIO
    from cStringIO import StringIO as cStringIO
except ImportError:
    from io import StringIO
    cStringIO = StringIO
import sys
import timeit
import os

try:
    import spitfire
    import spitfire.compiler.util
    import spitfire.compiler.options
except ImportError:
    spitfire = None

try:
    import Cheetah
    import Cheetah.Template
except ImportError:
    Cheetah = None

try:
    import django
    import django.conf
    import django.template
except ImportError:
    django = None

try:
    import jinja2
except ImportError:
    jinja2 = None

try:
    import mako
    import mako.template
except ImportError:
    mako = None

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')))
    import pyrender
except ImportError:
    pyrender = None

try:
    import tornado
    import tornado.template
except ImportError:
    tornado = None

try:
    import wheezy.template.engine
    import wheezy.template.loader
    import wheezy.template.ext.core
    import wheezy.html.utils
except ImportError:
    wheezy = None

try:
    import tenjin
except ImportError:
    tenjin = None

try:
    import gluon.html
    import gluon.template
except ImportError:
    gluon = None

try:
    import chameleon.zpt.template
except ImportError:
    chameleon = None

try:
    import bottle
except ImportError:
    bottle = None


TABLE_DATA = [
    dict(a=1,
         b=2,
         c=3,
         d=4,
         e=5,
         f=6,
         g=7,
         h=8,
         i=9,
         j=10) for x in range(1000)
]


def get_spitfire_tests():
    if not spitfire:
        return []

    tmpl_src = """
        <table>
            #for $row in $table
                <tr>
                    #for $column in $row.values()
                        <td>$column</td>
                    #end for
                </tr>
            #end for
        </table>
    """

    tmpl_search_list = [{'table': TABLE_DATA}]

    default_opts = spitfire.compiler.options.default_options
    o1_opts = spitfire.compiler.options.o1_options
    o2_opts = spitfire.compiler.options.o2_options
    o3_opts = spitfire.compiler.options.o3_options

    def _spitfire_baked_opts(o):
        o = copy.copy(o)
        o.baked_mode = True
        o.generate_unicode = False
        return o

    baked_opts = _spitfire_baked_opts(default_opts)
    baked_o1_opts = _spitfire_baked_opts(o1_opts)
    baked_o2_opts = _spitfire_baked_opts(o2_opts)
    baked_o3_opts = _spitfire_baked_opts(o3_opts)

    tmpl = spitfire.compiler.util.load_template(tmpl_src,
                                                'tmpl',
                                                analyzer_options=default_opts)

    tmpl_o1 = spitfire.compiler.util.load_template(tmpl_src,
                                                   'tmpl_o1',
                                                   analyzer_options=o1_opts)

    tmpl_o2 = spitfire.compiler.util.load_template(tmpl_src,
                                                   'tmpl_o2',
                                                   analyzer_options=o2_opts)

    tmpl_o3 = spitfire.compiler.util.load_template(tmpl_src,
                                                   'tmpl_o3',
                                                   analyzer_options=o3_opts)

    tmpl_baked = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked',
        analyzer_options=baked_opts)

    tmpl_baked_o1 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked_o1',
        analyzer_options=baked_o1_opts)

    tmpl_baked_o2 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked_o2',
        analyzer_options=baked_o2_opts)

    tmpl_baked_o3 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked_o3',
        analyzer_options=baked_o3_opts)

    tmpl_unfiltered = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered',
        analyzer_options=default_opts,
        compiler_options={'enable_filters': False})

    tmpl_unfiltered_o1 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered_o1',
        analyzer_options=o1_opts,
        compiler_options={'enable_filters': False})

    tmpl_unfiltered_o2 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered_o2',
        analyzer_options=o2_opts,
        compiler_options={'enable_filters': False})

    tmpl_unfiltered_o3 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered_o3',
        analyzer_options=o3_opts,
        compiler_options={'enable_filters': False})

    def test_spitfire():
        """Spitfire template"""
        tmpl(search_list=tmpl_search_list).main()

    def test_spitfire_o1():
        """Spitfire template -O1"""
        tmpl_o1(search_list=tmpl_search_list).main()

    def test_spitfire_o2():
        """Spitfire template -O2"""
        tmpl_o2(search_list=tmpl_search_list).main()

    def test_spitfire_o3():
        """Spitfire template -O3"""
        tmpl_o3(search_list=tmpl_search_list).main()

    def test_spitfire_baked():
        """Spitfire template baked"""
        tmpl_baked(search_list=tmpl_search_list).main()

    def test_spitfire_baked_o1():
        """Spitfire template baked -O1"""
        tmpl_baked_o2(search_list=tmpl_search_list).main()

    def test_spitfire_baked_o2():
        """Spitfire template baked -O2"""
        tmpl_baked_o2(search_list=tmpl_search_list).main()

    def test_spitfire_baked_o3():
        """Spitfire template baked -O3"""
        tmpl_baked_o3(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered():
        """Spitfire template unfiltered"""
        tmpl_unfiltered(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered_o1():
        """Spitfire template unfiltered -O1"""
        tmpl_unfiltered_o2(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered_o2():
        """Spitfire template unfiltered -O2"""
        tmpl_unfiltered_o2(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered_o3():
        """Spitfire template unfiltered -O3"""
        tmpl_unfiltered_o3(search_list=tmpl_search_list).main()

    return [
        test_spitfire,
        test_spitfire_o1,
        test_spitfire_o2,
        test_spitfire_o3,
        test_spitfire_baked,
        test_spitfire_baked_o1,
        test_spitfire_baked_o2,
        test_spitfire_baked_o3,
        test_spitfire_unfiltered,
        test_spitfire_unfiltered_o1,
        test_spitfire_unfiltered_o2,
        test_spitfire_unfiltered_o3,
    ]


def get_python_tests():
    tmpl_table = string.Template('<table>\n$table\n</table>\n')
    tmpl_row = string.Template('<tr>\n$row\n</tr>\n')
    tmpl_column = string.Template('<td>$column</td>\n')

    def _buffer_fn(write, table):
        write('<table>\n')
        for row in table:
            write('<tr>\n')
            for column in row.values():
                write('<td>')
                write('%s' % column)
                write('</td>\n')
            write('</tr>\n')
        write('</table>\n')

    def test_python_template():
        """Python string template"""
        rows = ''
        for row in TABLE_DATA:
            columns = ''
            for column in row.values():
                columns = columns + tmpl_column.substitute(column=column)
            rows = rows + tmpl_row.substitute(row=columns)
        return tmpl_table.substitute(table=rows)

    def test_python_stringio():
        """Python StringIO buffer"""
        buffer = StringIO()
        _buffer_fn(buffer.write, TABLE_DATA)
        return buffer.getvalue()

    def test_python_cstringio():
        """Python cStringIO buffer"""
        buffer = cStringIO()
        _buffer_fn(buffer.write, TABLE_DATA)
        return buffer.getvalue()

    def test_python_list():
        """Python list concatenation"""
        buffer = []
        _buffer_fn(buffer.append, TABLE_DATA)
        return ''.join(buffer)

    return [
        test_python_template,
        test_python_stringio,
        test_python_cstringio,
        test_python_list,
    ]


def get_cheetah_tests():
    if not Cheetah:
        return []

    tmpl_src = """
        <table>
            #for $row in $table
                <tr>
                    #for $column in $row.values()
                        <td>$column</td>
                    #end for
                </tr>
            #end for
        </table>
    """

    tmpl_search_list = [{'table': TABLE_DATA}]

    tmpl = Cheetah.Template.Template(tmpl_src, searchList=tmpl_search_list)

    def test_cheetah():
        """Cheetah template"""
        tmpl.respond()

    return [
        test_cheetah,
    ]


def get_django_tests():
    if not django:
        return []

    django.conf.settings.configure()
    django.setup()

    tmpl_src = """
        <table>
            {% for row in table %}
                <tr>
                    {% for column in row.values %}
                        <td>{{ column }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    """
    tmpl_autoescaped_src = ('{% autoescape on %}' +
                            tmpl_src +
                            '{% endautoescape %}')

    engine = django.template.Engine()
    tmpl = django.template.Template(tmpl_src, engine=engine)
    tmpl_autoescaped = django.template.Template(tmpl_autoescaped_src, engine=engine)

    tmpl_context = django.template.Context({'table': TABLE_DATA})

    def test_django():
        """Django template"""
        tmpl.render(tmpl_context)

    def test_django_autoescaped():
        """Django template autoescaped"""
        tmpl_autoescaped.render(tmpl_context)

    return [
        test_django,
        test_django_autoescaped,
    ]


def get_jinja2_tests():
    if not jinja2:
        return []

    tmpl_src = """
        <table>
            {% for row in table %}
                <tr>
                    {% for column in row.values() %}
                        <td>{{ column }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    """

    tmpl = jinja2.Template(tmpl_src)
    tmpl_autoescaped = jinja2.Template(tmpl_src, autoescape=True)

    def test_jinja2():
        """Jinja2 template"""
        tmpl.render(table=TABLE_DATA)

    def test_jinja2_autoescaped():
        """Jinja2 template autoescaped"""
        tmpl_autoescaped.render(table=TABLE_DATA)

    return [
        test_jinja2,
        test_jinja2_autoescaped,
    ]


def get_mako_tests():
    if not mako:
        return []

    tmpl_src = """
        <table>
            % for row in table:
                <tr>
                    % for column in row.values():
                        <td>${column}</td>
                    % endfor
                </tr>
            % endfor
        </table>
    """

    tmpl = mako.template.Template(tmpl_src)
    tmpl_autoescaped = mako.template.Template(tmpl_src, default_filters=['h'])

    def test_mako():
        """Mako template"""
        tmpl.render(table=TABLE_DATA)

    def test_mako_autoescaped():
        """Mako template autoescaped"""
        tmpl_autoescaped.render(table=TABLE_DATA)

    return [
        test_mako,
        test_mako_autoescaped,
    ]


def get_pyrender_tests():
    if not pyrender:
        return []

    tmpl_src = """
        <table>
            {% for row in table %}
                <tr>
                    {% for column in row.values() %}
                        <td>{{ column }}</td>
                    {% end %}
                </tr>
            {% end %}
        </table>
    """

    tmpl = pyrender.Compiler().compile(tmpl_src)
    context = {'table': TABLE_DATA}

    def test_pyrender():
        """pyrender template"""
        tmpl.render(context)

    return [test_pyrender]


def get_tornado_tests():
    if not tornado:
        return []

    tornado_template = tornado.template.Template("""\
<table>
    {% for row in table %}
    <tr>
        {% for key, value in row.items() %}
        <td>{{ key }}</td><td>{{ value }}</td>
        {% end %}
    </tr>
    {% end %}
</table>
""")

    def test_tornado():
        """tornado template"""
        return tornado_template.generate(table=TABLE_DATA).decode('utf8')

    return [
        test_tornado,
    ]


def get_wheezy_tests():
    if not wheezy:
        return []

    from wheezy.template.engine import Engine
    from wheezy.template.loader import DictLoader
    from wheezy.template.ext.core import CoreExtension
    # from wheezy.html.utils import escape_html as escape

    engine = Engine(loader=DictLoader({'x': """\
@require(table)
<table>
    @for row in table:
    <tr>
        @for key, value in row.items():
        <td>@key!s</td><td>@value!s</td>
        @end
    </tr>
    @end
</table>
"""}), extensions=[CoreExtension()])
    # engine.global_vars.update({'h': escape})
    wheezy_template = engine.get_template('x')

    ctx = {'table': TABLE_DATA}

    def test_wheezy_template():
        """wheezy template"""
        return wheezy_template.render(ctx)

    return [
        test_wheezy_template,
    ]


def get_tenjin_tests():
    if not tenjin:
        return []

    try:
        import webext
        helpers = {
            'to_str': webext.to_str,
            'escape': webext.escape_html
        }
    except ImportError:
        helpers = {
            'to_str': tenjin.helpers.to_str,
            'escape': tenjin.helpers.escape
        }
    tenjin_template = tenjin.Template(encoding='utf8')
    tenjin_template.convert("""\
<table>
    <?py for row in table: ?>
    <tr>
        <?py for key, value in row.items(): ?>
        <td>${ key }</td><td>#{ value }</td>
        <?py #end ?>
    </tr>
    <?py #end ?>
</table>
""")

    ctx = {
        'table': TABLE_DATA,
    }

    def test_tenjin():
        """tenjin template"""
        return tenjin_template.render(ctx, helpers)

    return [
        test_tenjin,
    ]


def get_web2py_tests():
    if not gluon:
        return []

    import cStringIO
    from gluon.html import xmlescape
    from gluon.template import get_parsed

    # see gluon.globals.Response
    class DummyResponse(object):
        def __init__(self):
            self.body = cStringIO.StringIO()

        def write(self, data, escape=True):
            if not escape:
                self.body.write(str(data))
            else:
                self.body.write(xmlescape(data))

    web2py_template = compile(get_parsed("""\
<table>
    {{ for row in table: }}
    <tr>
        {{ for key, value in row.items(): }}
        <td>{{ =key }}</td><td>{{ =value }}</td>
        {{ pass }}
    </tr>
    {{ pass }}
</table>
"""), '', 'exec')

    ctx = {'table': TABLE_DATA}

    def test_web2py():
        """web2pu template"""
        response = DummyResponse()
        exec(web2py_template, {}, dict(response=response, **ctx))
        return response.body.getvalue().decode('utf8')

    return [
        test_web2py,
    ]


def get_chameleon_tests():
    if not chameleon:
        return []

    from chameleon.zpt.template import PageTemplate
    chameleon_template = PageTemplate("""\
<table>
    <tr tal:repeat="row table">
        <i tal:omit-tag="" tal:repeat="key row">
        <td>${key}</td><td>${row[key]}</td>
        </i>
    </tr>
</table>
""")

    ctx = {'table': TABLE_DATA}

    def test_chameleon():
        """chameleon"""
        return chameleon_template.render(**ctx)

    return [
        test_chameleon,
    ]


def get_bottle_tests():
    if not bottle.SimpleTemplate:
        return []

    from bottle import SimpleTemplate

    bottle_template = SimpleTemplate("""\
<table>
    % for row in table:
    <tr>
        % for key, value in row.items():
        <td>{{key}}</td><td>{{!value}}</td>
        % end
    </tr>
    % end
</table>
""")

    def test_bottle():
        """bottle"""
        return bottle_template.render(table=TABLE_DATA)

    return [
        test_bottle,
    ]


def time_test(test, number):
    # Put the test in the global scope for timeit.
    name = 'timeit_%s' % test.__name__
    globals()[name] = test
    # Time the test.
    timer = timeit.Timer(setup='from __main__ import %s;' % name,
                         stmt='%s()' % name)
    time = timer.timeit(number=number) / number
    if time < 0.00001:
        result = '   (not installed?)'
    else:
        result = '%16.2f ms' % (1000 * time)
    print('%-35s %s' % (test.__doc__, result))


def run_tests(which=None, number=100, compare=False):
    if number > 100:
        print('Running benchmarks %d times each...' % number)
        print('')
    if compare:
        groups = [
            'bottle',
            'chameleon',
            'cheetah',
            'django',
            'jinja2',
            'mako',
            'pyrender',
            'python',
            'spitfire',
            'tenjin',
            'tornado',
            'web2py',
            'wheezy',
        ]
    else:
        groups = ['pyrender']
    # Built the full list of eligible tests.
    tests = []
    missing_engines = []
    for g in groups:
        test_list_fn = 'get_%s_tests' % g
        test = globals()[test_list_fn]()
        if test:
            tests.extend(test)
        else:
            missing_engines.append(g)
    # Optionally filter by a set of matching test name (sub)strings.
    if which:
        which_tests = []
        for t in tests:
            for w in which:
                if w.lower() in t.__name__.lower():
                    which_tests.append(t)
        tests = which_tests
    # Report any missing template engines.
    if missing_engines:
        sys.stderr.write(
            'The following template engines are not installed and will be '
            'skipped in the benchmark: %r\n' % missing_engines)
    # Run the tests.
    for t in tests:
        time_test(t, number)


def profile_tests(which=None):
    print('Profiling...')
    print('')
    import hotshot, hotshot.stats
    profile_data = 'template.prof'
    profile = hotshot.Profile(profile_data)
    profile.runcall(run_tests, which=which, number=1, compare=False)
    stats = hotshot.stats.load(profile_data)
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    print('')
    stats.print_stats()
    print('Profile data written to %s' % profile_data)


def main():
    option_parser = optparse.OptionParser()
    option_parser.add_option('-n', '--number', type='int', default=100)
    option_parser.add_option('-c',
                             '--compare',
                             action='store_true',
                             default=False)
    option_parser.add_option('-p',
                             '--profile',
                             action='store_true',
                             default=False)
    (options, args) = option_parser.parse_args()

    if options.profile:
        profile_tests(which=args)
    else:
        run_tests(which=args, number=options.number, compare=options.compare)


if __name__ == '__main__':
    main()
