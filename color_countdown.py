#!/usr/bin/env python3

import time
import curses
from font import font, font_len
#debug
# from parser_args import ...

total_time = 0
color_list = ( 0, 224, 217, 203, 197  )
color_borders = ( 50, 30, 15, 5, 0 )
single_color = -2
exit_code = 1

def color_number( left ):
    for i, percent in enumerate(color_borders) :
        if left >= total_time * percent /100 :
            return color_list[ i ]
    return color_list[ 0 ]
        
def gen_text( seconds ):
    m, s = divmod( seconds, 60 )
    h,m = divmod( m, 60 )
    if h > 0 :
        t = f"{h}:{m:02}:{s:02}"
    else :
        t = f"{m:02}:{s:02}"
    out_str = [''] * font_len
    for line in range( font_len ):
        for znak in t:
            out_str[line] = out_str[line] + font[ znak ][ line ]
    return out_str

def main(stdscr : curses.window ):
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay( True )
    curses.curs_set( False )
    global exit_code 
    exit_code = 0
   # define all colors because selective define doesn't works corectly
   # at least in my tests
    for i in range( 1, 254 ):
        curses.init_pair( i + 1,  i, -1)

    if single_color > -2:
        curses.init_pair( 1, single_color, -1 )

    term_size = stdscr.getmaxyx() 
    x_pos =int( term_size[0] / 2 ) - font_len // 2
    y_pos = int( term_size[1] / 2 )
    start_time = time.monotonic()
    stop_time = start_time + total_time
    step = 1
    
    try:
        time_left = int( stop_time - time.monotonic() )
        key = stdscr.getch()
        last_len = 0 
        while (time_left >= 0) : 
            delta = time.monotonic()
            t = gen_text(time_left)
            t_len = len(t[0])
            
            key = stdscr.getch() 
            if key == 27 or key == ord('q') or key == ord('Q') or key == 3:
                exit_code = 1
                break
            time.sleep(0.3)
            if term_size != stdscr.getmaxyx(): 
                term_size = stdscr.getmaxyx() 
                x_pos =int( term_size[0] / 2 ) - font_len // 2
                y_pos = int( term_size[1] / 2 )
                stdscr.clear()
                last_len = t_len
            if last_len > t_len :
                padding = " " *(last_len - t_len)
                front = " " * (last_len // 2 - t_len // 2)
            else : 
                padding = ""
                front = ""
            selected_color =  curses.color_pair( color_number( time_left ) )
            for line in range(font_len):
                if last_len > t_len :
                    stdscr.addstr( x_pos + line, y_pos - last_len // 2,  front, selected_color ) 
                stdscr.addstr( x_pos + line, y_pos - t_len // 2,  t[line] + padding, selected_color )
            
            stdscr.refresh()
            delta = time.monotonic()-delta
            time.sleep( step - delta )
            time_left = int( stop_time - time.monotonic() )
            last_len = t_len
			
    except KeyboardInterrupt:
        exit_code = 3
    except curses.ERR:
        exit_code = 2
    
def help():  
    print( f"""Usage:
    {sys.argv[0]} <time> [color]
        where <time> - time in seconds or  XXsXXmXXh ex. 1h10m20s
              color - one from the standard color list: 
                    --white, --black, --red, --green, --blue,
                    --cyan, --magenta, --yellow, --default 
    to quit pres ESC or 'q'  """)
  
def read_config(fname):
    import json
    try:
        with open( 'color_countdown.json' ) as f:
            data = json.load( f )
    except Exception as e:
        data = None
    
    cl_list = list()
    cl_borders = list()
    if data != None:
        try:
            main_colors = data['colors']
            for range in main_colors:
                cl_borders.append(int(range))
                cl_list.append(main_colors[range])
            return ( cl_list, cl_borders )
        except Exception as e:
            pass
    if len(cl_list) == 0:
        return ( color_list, color_borders )
            


if __name__ ==  "__main__":
    import sys 
    from parser_args import parse_time, parse_colors 

    color_list, color_borders  = read_config('color_countdown.json')
        
    if len(sys.argv) < 2 :
        help()
        exit(1)
    try:
        total_time = parse_time( sys.argv[1] )
        if len(sys.argv) > 2 :
            res = parse_colors( sys.argv[2:] )
            if len( res[1] ) > 0:
                print(f"Wrong option(s) {res[1]}")
                help()
                exit(1)
            if res[0] >= -1:
                color_list = ( 1, )
                color_borders = ( 0, )
                single_color = res[0]
        curses.wrapper( main )
    except Exception as e:
         print(f"{type(e)} {e}")
         exit(1)
    exit( exit_code )



