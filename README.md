# color_countdown
---
Countdown script for linux terminal with counter changing color from white to red.
Written in python as a simple script.
Idea taken from https://github.com/antonmedv/countdown with added text coloring over time and the ability to configure colors.
        
### Prerequisites
Requires python 3.x installed. The only libraries used are sys, time, curses, which are installed by default with python 3 on typical systems (at least they are for me :smile: ).
 
## Install
To install, just copy the repository to any directory.
Optionally, you can give color_countdown.py a executable attribute
``` chmod u+x color_countdown.py ```

## Run
To run in terminal go to the directory of your choice and type ``./color_countdown <TIME>`` e.g.

```./color_countdown 10 ```

or (if you didn't give executable attribute)

``` python3 color_countdown 10 ```

To stop just press ESC, Q key or Ctrl-C.
If countdown ends with end of time it returns exit code 0, otherwise another value. 
So you can conditionally run any program at te end e.g.

```./color_countdown 10 && sl```

Running the script without options displays a hint on how to use it.

Running time can be set
* in seconds - any reasonable number (tested on 999999999, but it is not a reasonable number),
* or as **xxxHyyyMzzzS**, where xxx,yyy,zzz are the values of hours, minutes and seconds.


## Optional configuration file
The ***color_countdown.json*** file is optional and defines when and what color should be used.
The structure of this file is

```
{
  "colors" : {
    <percent_remaining>: <color_number>,
  }
}
```
color_number - is the standard color number in the terminal (or at least it was supposed to be) except "0" - it's the default color

Sample ***color_countdown.json*** with default palette:

```
{
    "colors" : {
        "50": 0,
        "30": 224,
        "15": 217,
        "5": 203,
        "0": 197        
    }
}
```

