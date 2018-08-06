# pyrender

A Python template rendering engine.

## Todo

* use unicode on py2
* extention and blocks
* includes + inlines
* tests
* add to pip

## Benchmarks

`bigtable.py` run on 2015 MBP 15"

    CPython 2.7.10              msec    rps  tcalls  funcs
    bottle 0.12.13             32.50  30.77  163014     21
    chameleon 3.4              36.08  27.72  161032     22
    cheetah 2.4.4              74.99  13.34  225018     20
    django 1.11.15            347.30   2.88 1162080     62
    jinja2 2.10                19.40  51.54   61018     25
    list_append                 6.07 164.75   63006      7
    list_extend                 4.94 202.43   23006      7
    mako 1.0.7                 17.90  55.87   93034     35
    pyrender                    5.85 171.06   63009     10
    spitfire 0.7.15            16.29  61.39   74014     20
    tenjin 1.1.1               11.20  89.27   73009     12
    tornado 5.1                37.35  26.77  233020     21
    web2py 2.1.1               81.06  12.34  295014     18
    wheezy_template 0.1.167     5.95 168.19   63008      9

    CPython 3.6.4               msec    rps  tcalls  funcs
    bottle 0.12.13             20.29  49.29  133015     19
    chameleon 3.4              35.53  28.14  182034     23
    django 2.1                214.93   4.65  815081     60
    jinja2 2.10                17.87  55.95   61021     27
    list_append                5.57 179.62   63007      8
    list_extend                4.44 225.11   23007      8
    mako 1.0.7                 18.35  54.49   93035     36
    pyrender                    5.67 176.52   63010     11
    tenjin 1.1.1               10.49  95.36   73011     13
    tornado 5.1                47.81  20.91  353025     24
    wheezy_template 0.1.167     5.78 173.04   63009     10
