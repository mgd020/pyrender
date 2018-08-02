# pyrender

A Python template rendering engine.

## Todo

* escape single quotes and newlines

## Benchmarks

`bigtable.py` run on 2015 MBP 15"

    CPython 2.7.10              msec    rps  tcalls  funcs
    bottle 0.12.13             34.16  29.28  163016     23
    chameleon 3.4              35.55  28.13  161033     24
    cheetah 2.4.4              75.03  13.33  225019     22
    pyrender                    6.99 142.99   53009      9
    django 1.11.15            365.38   2.74 1162081     64
    jinja2 2.10                20.79  48.10   61019     27
    list_append                 6.08 164.39   63007      9
    list_extend                 6.04 165.65   23007      9
    mako 1.0.7                 20.60  48.55   93035     36
    tenjin 1.1.1                7.74 129.22   43010     13
    tornado 5.1                37.68  26.54  233021     23
    web2py 2.1.1               76.66  13.04  295015     20
    wheezy_template 0.1.167     5.95 168.16   63009     11

    CPython 3.6.4               msec    rps  tcalls  funcs
    bottle 0.12.13             21.65  46.19  133017     21
    chameleon 3.4              37.67  26.55  182035     25
    custom                      7.99 125.13   53011     10
    django 2.1                218.37   4.58  815082     62
    jinja2 2.10                19.01  52.59   61022     29
    list_append                24.63  40.59  103008     12
    list_extend                23.19  43.11   63008     12
    mako 1.0.7                 19.74  50.65   93036     37
    tenjin 1.1.1               19.04  52.53  123012     16
    tornado 5.1                53.00  18.87  353026     26
    wheezy_template 0.1.167    25.11  39.83  103010     14
