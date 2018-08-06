# pyrender

A Python template rendering engine.

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
    list_extend          5.28 189.56   23006      7
    list_append          5.89 169.86   63006      7
    wheezy_template      6.09 164.24   63008      9
    pyrender             6.57 152.10   63019     16
    tenjin              12.16  82.25   73009     12
    spitfire            16.94  59.03   74014     20
    mako                19.48  51.35   93034     35
    jinja2              20.58  48.60   61018     25
    bottle              32.16  31.10  163014     21
    chameleon           33.00  30.30  161032     22
    tornado             34.90  28.65  233020     21
    cheetah             72.70  13.75  225018     20
    web2py              77.22  12.95  295014     18
    django             353.94   2.83 1162080     62

    CPython 3.6.4        msec    rps  tcalls  funcs
    list_extend          4.34 230.62   23007      8
    pyrender             5.45 183.51   63020     17
    wheezy_template      5.49 182.26   63009     10
    list_append          5.53 180.77   63007      8
    tenjin              10.25  97.61   73011     13
    jinja2              17.92  55.80   61021     27
    mako                18.24  54.83   93035     36
    bottle              21.78  45.90  133015     19
    chameleon           34.98  28.59  182034     23
    tornado             47.71  20.96  353025     24
    django             205.85   4.86  815081     60

### `render_benchmark`

    CPython 2.7.10                                  msec
    pyrender template                               2.56
    Python list concatenation                       2.62
    Spitfire template unfiltered -O3                3.15
    Spitfire template unfiltered -O1                3.24
    Spitfire template unfiltered -O2                3.43
    Mako template                                   3.51
    Jinja2 template                                 5.75
    Spitfire template -O3                           7.76
    wheezy template                                 7.81
    Spitfire template -O2                           8.00
    Python cStringIO buffer                         8.33
    Spitfire template unfiltered                    8.49
    Spitfire template baked -O3                     9.49
    Spitfire template baked -O1                     9.81
    Spitfire template baked -O2                     9.83
    Mako template autoescaped                      11.09
    Spitfire template -O1                          11.27
    Spitfire template                              13.26
    Jinja2 template autoescaped                    14.18
    Spitfire template baked                        15.63
    Cheetah template                               18.22
    tenjin template                                20.20
    Python StringIO buffer                         23.77
    Python string template                         23.87
    tornado template                               32.50
    chameleon                                      33.37
    bottle                                         34.65
    web2pu template                                69.57
    Django template autoescaped                   152.97
    Django template                               154.07

    CPython 3.6.4                                   msec
    Python list concatenation                       3.34
    Python StringIO buffer                          3.74
    pyrender template                               3.77
    Mako template                                   4.83
    wheezy template                                 6.62
    Jinja2 template                                 6.80
    Mako template autoescaped                      12.42
    tenjin template                                18.31
    Jinja2 template autoescaped                    19.05
    bottle                                         22.50
    Python string template                         29.83
    chameleon                                      40.55
    tornado template                               51.84
    Django template autoescaped                   122.51
    Django template                               122.86
