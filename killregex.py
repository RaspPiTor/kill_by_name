#!/usr/bin/env python3
import argparse
import os
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('regex')
    parser.add_argument('-s', '--signal', default='15', type=int)
    parser.add_argument('-c', '--cmdline', action='store_true')
    args = parser.parse_args()
    regex = re.compile(args.regex)
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    ending = ['comm', 'cmdline'][int(args.cmdline)]
    for pid in pids:
        try:
            with open(os.path.join('/proc', pid, ending)) as file:
                result = file.read().rstrip('\x00').strip()
            if regex.fullmatch(result):
                print('Found match', pid, result)
                os.kill(int(pid), args.signal)
        except IOError:
            pass

if __name__ == '__main__':
    main()
