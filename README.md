# pyrender

A Python template rendering engine.

## Features

* fast
* lightweight
* simple
* no dependencies
* templates compiled to Python bytecode
* full syntax supported
* auto-indenting with `end` keyword (no `:`)
* eval `{{ ... }}` and exec `{% ... %}` tokens

## Example

`template.html`

```python
from pyrender.template import Template

source = """\
{% import sys, getpass %}

<h1>{{ title }}</h1>

<p>Hi {{ getpass.getuser() or 'you' }}</p>

<h2>Items</h2>

<ul>{% for item in items %}
    <li>{{ item }}</li>{% end %}
</ul>

<p>{{ sys.version }}</p>
"""

template = Template(source)

print(template.render({
    'title': 'Shopping List',
    'items': [
        'eggs',
        'milk',
        'break',
    ],
}))
```

`stdout`

```html
<h1>Shopping List</h1>

<p>Hi matt</p>

<ul>
    <li>eggs</li>
    <li>milk</li>
    <li>break</li>
</ul>

<p>2.7.14 (default, Mar  9 2018, 23:57:12) 
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]</p>
```

## Todo

* use unicode on py2
* extention and blocks
* includes + inlines
* tests
* add to pip

## Benchmarks

Run on 2017 MBP 15".

### `bigtable`

    CPython 2.7.10       msec    rps  tcalls  funcs
    list_extend          5.20 192.40   23006      7
    list_append          5.28 189.49   63006      7
    pyrender             6.57 152.19   63018     15
    wheezy_template      6.59 151.63   63008      9
    tenjin              11.13  89.85   73009     12
    spitfire            16.80  59.54   74014     20
    jinja2              18.34  54.52   61018     25
    mako                18.52  53.99   93034     35
    tornado             33.63  29.74  233020     21
    bottle              34.42  29.05  163014     21
    chameleon           35.09  28.50  161032     22
    web2py              75.28  13.28  295014     18
    cheetah             78.11  12.80  225018     20
    django             339.64   2.94 1162080     62

    CPython 3.6.4        msec    rps  tcalls  funcs
    list_extend          4.64 215.54   23007      8
    list_append          5.89 169.69   63007      8
    pyrender             5.98 167.34   63019     16
    wheezy_template      6.34 157.65   63009     10
    tenjin              11.97  83.57   73011     13
    jinja2              18.85  53.05   61021     27
    mako                19.95  50.12   93035     36
    bottle              22.40  44.65  133015     19
    chameleon           38.64  25.88  182034     23
    tornado             54.73  18.27  353025     24
    django             227.06   4.40  815081     60

### `render_benchmark`

    CPython 2.7.10                                  msec
    pyrender template                               2.71
    Python list concatenation                       2.96
    Spitfire template unfiltered -O3                3.00
    Mako template                                   4.01
    Spitfire template unfiltered -O2                3.32
    Spitfire template unfiltered -O1                3.35
    Jinja2 template                                 7.22
    Spitfire template -O3                           7.26
    wheezy template                                 7.46
    Spitfire template unfiltered                    7.51
    Spitfire template -O2                           7.58
    Python cStringIO buffer                         8.36
    Spitfire template baked -O3                     8.66
    Spitfire template baked -O2                     8.97
    Spitfire template baked -O1                     9.02
    Spitfire template -O1                          11.06
    Mako template autoescaped                      11.76
    Spitfire template                              12.59
    Spitfire template baked                        14.71
    Jinja2 template autoescaped                    16.85
    tenjin template                                19.53
    Cheetah template                               22.45
    Python StringIO buffer                         23.25
    Python string template                         24.35
    tornado template                               32.00
    bottle                                         36.92
    chameleon                                      39.10
    web2pu template                                68.74
    Django template autoescaped                   165.65
    Django template                               171.15

    CPython 3.6.4                                   msec
    pyrender template                               3.32
    Python list concatenation                       3.51
    Python StringIO buffer                          3.53
    Mako template                                   3.59
    Python cStringIO buffer                         4.02
    Jinja2 template                                 5.15
    wheezy template                                 5.96
    Mako template autoescaped                      11.24
    Jinja2 template autoescaped                    14.28
    tenjin template                                20.31
    bottle                                         21.58
    Python string template                         27.36
    chameleon                                      40.25
    tornado template                               50.36
    Django template autoescaped                   110.66
    Django template                               126.38
