#!/usr/bin/env python3

import re

#parse string reprezenting time to convert to time in seconds
def parse_time( text_to_parse ) :
    h_pattern = "\d+h"
    m_pattern = "\d+m"
    s_pattern = "\d+s"
    s_pat2 = "^\d+$"
    text_to_parse = text_to_parse.lower()
    seconds_all = re.findall(s_pat2, text_to_parse )
    if len(seconds_all) == 1 :
        return int(seconds_all[0])
    hours = re.findall(h_pattern, text_to_parse )
    minutes = re.findall(m_pattern, text_to_parse )
    seconds = re.findall(s_pattern, text_to_parse )
    text_left = re.sub(h_pattern, '', text_to_parse )
    text_left = re.sub(m_pattern, '', text_left )
    text_left = re.sub(s_pattern, '', text_left )

    # print(hours, minutes, seconds, seconds_all)
    if len(seconds) > 1 or len(minutes) >1 or len(hours) > 1 or len(text_left)>0 or len(text_to_parse) == 0 :
        raise Exception('Invalid time definition string format')
    res = 0
    if len(seconds) == 1:
        res += int( seconds[0][:-1])
    if len(minutes) == 1:
        res += int( minutes[0][:-1])*60
    if len(hours) == 1:
        res += int( hours[0][:-1])*3600
    return res    


# parse arguments setting single color
# result tuple of color number and list of arguments left, but witout color defs
# if many colors are on the list, the last one is valid
def parse_colors( args ):
    import curses
    import curses
    colors = {
        '--white': curses.COLOR_WHITE,
        '--black': curses.COLOR_BLACK,
        '--red': curses.COLOR_RED,
        '--green': curses.COLOR_GREEN,
        '--blue': curses.COLOR_BLUE,
        '--cyan': curses.COLOR_CYAN,
        '--magenta': curses.COLOR_MAGENTA,
        '--yellow': curses.COLOR_YELLOW,
        '--default': -1
    }
    
    args_left = list(args)
    res = -2
    for ar in args : 
        a = ar.lower()
        if colors.get( a ) != None :
            res = colors[ a ]
            args_left.remove( ar )
            # print( f"color {res} ")
    return ( res, args_left )

if __name__ == '__main__':
    import sys
    try :
        if len(sys.argv) == 1:
            print( parse_time('999') )
            print( parse_time("20s") )
            print( parse_time("30m") )
            print( parse_time("100h") )
            print( parse_time('20h10m400s'))
        else:
            print( parse_time( sys.argv[1] ) )
            if len( sys.argv ) > 2:
                print( parse_colors( sys.argv[2:] ) )
    except Exception as e:
        print(f" --> {type(e)} {e}")