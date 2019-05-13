class level:
    debug   = 0
    warning = 1
    error   = 2
    info    = 3

prefix_d = "[+]DEBUG > "
prefix_w = "[!]WARN  > "
prefix_i = "[+]INFO  > "
prefix_e = "[!]ERROR > "

colour_table = {'blue':    '38;2;162;191;244m',
                'default': '38;2;196;196;196m',
                'green':   '38;2;204;250;158m',
                'yellow':  '38;2;255;255;102m',
                'red':     '38;2;255;51;51m'
               }

def debug_log(string, debug_level, spaced=False):
    #truecolour_esc = '\x1b[{}m{}\x1b[0m'
    esc_sequence  = "\x1b[{}{}\x1b[0m{}"
    if debug_level == level.debug:
        colour = colour_table['green']
        prefix = prefix_d
    elif debug_level == level.warning:
        colour = colour_table['yellow']
        prefix = prefix_w
    elif debug_level == level.info:
        colour = colour_table['blue']
        prefix = prefix_i
    elif debug_level == level.error:
        colour = colour_table['red']
        prefix = prefix_e
    else:
        colour = colour_table['default']
        prefix = prefix_d
    print(esc_sequence.format(colour, prefix, string))

