#!/usr/bin/env python3

import json
import subprocess
import argparse


def get_args():
    parser = argparse.ArgumentParser('ワークスペース移動')
    parser.add_argument('-d','--direction',choices=['left','right'], required=True)
    parser.add_argument('-m','--move',action='store_true')
    return parser.parse_args()


def main():
    args = get_args()
    move = args.move
    direction = args.direction

    ws_list = get_wslist()
    cur_ws = get_cur_ws()
    new_ws = get_new_ws(cur_ws, ws_list, direction)

    cmd = ''
    if move:
        cmd += f'i3-msg move container to workspace {new_ws} && '
    cmd += f'i3-msg workspace {new_ws}'
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)



def get_wslist():
    base_wslist = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    cmd = 'i3-msg -t get_workspaces'
    active_wsjson = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout
    active_wslist = [d.get('name') for d in json.loads(active_wsjson)]
    active_wslist = [n for n in active_wslist if not n in base_wslist]

    ws_list = base_wslist + active_wslist
    return ws_list



def get_cur_ws():
    cmd = 'i3-msg -t get_workspaces'
    active_wsjson = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout
    cur_ws = [d.get('name') for d in json.loads(active_wsjson) if d.get('focused') == True][0]
    return cur_ws



def get_new_ws(cur_ws, ws_list, direction):
    ws_index = ws_list.index(cur_ws)
    if direction == 'right':
        ws_index += 1
    else:
        ws_index -= 1
    if ws_index > len(ws_list)-1:
        ws_index = 0
    elif ws_index < 0:
        ws_index = len(ws_list)-1
    new_ws = ws_list[ws_index]
    return new_ws



main()
