#!/usr/bin/python2


import argparse
from random import randint


NUM_TRACKS = 48


tracks = {
  "new": [
    {
      "cup": "Mushroom",
      "tracks": [
        "Mario Kart Stadium",
        "Water Park",
        "Sweet Sweet Canyon",
        "Thwomp Ruins"
        ]},
    {
      "cup": "Flower",
      "tracks": [
        "Mario Circuit",
        "Toad Harbor",
        "Twisted Mansion",
        "Shy Guy Falls"
        ]},
    {
      "cup": "Star",
      "tracks": [
        "Sunshine Airport",
        "Dolphin Shoals",
        "Electrodrome",
        "Mount Wario"
        ]},
    {
      "cup": "Special",
      "tracks": [
        "Butttop Cruise",
        "Bone Dry Dunes",
        "Bowser's Castle",
        "Rainbow Road"
        ]}],
  "retro": [
    {
      "cup": "Shell",
      "tracks": [
        "Wii Moo Moo Meadows",
        "GBA Mario Circuit",
        "DS Cheep Cheep Beach",
        "N64 Toad's Turnpike"
        ]},
    {
      "cup": "Banana",
      "tracks": [
        "GCN Dry Dry Desert",
        "SNES Donut Plains 3",
        "N64 Royal Raceway",
        "3DS DK Jungle"
        ]},
    {
      "cup": "Leaf",
      "tracks": [
        "DS Wario Stadium",
        "GCN Sherbet Land",
        "3DS Music Park",
        "N64 Yoshi Valley"
        ]},
    {
      "cup": "Lightning",
      "tracks": [
        "DS Tick Tock Clock",
        "3DS Piranha Plant Slide",
        "Wii Grumble Volcano",
        "N64 Rainbow Road"
        ]}],
  "dlc": [
    {
      "cup": "Egg",
      "tracks": [
        "GCN Yoshi's Circuit",
        "Excitebike Arena",
        "Dragon Driftway",
        "Mute City"
        ]},
    {
      "cup": "Triforce",
      "tracks": [
        "Wii Wario's Gold Mine",
        "SNES Rainbow Road",
        "Ice Ice Outpost",
        "Hyrule Circuit"
        ]},
    {
      "cup": "Bell",
      "tracks": [
        "3DS Neo Bowser City",
        "GBA Ribbon Road",
        "Super Bell Subway",
        "Big Blue"
        ]},
    {
      "cup": "Crossing",
      "tracks": [
        "GCN Baby Park",
        "GBA Cheese Land",
        "Wild Woods",
        "Animal Crossing"
        ]}]}


def track_from_idx(tracks, idx):
    if idx <= 16:
        return track_from_cat(tracks['new'], idx)
    if idx <= 32:
        return track_from_cat(tracks['retro'], idx-16)
    else:
        return track_from_cat(tracks['dlc'], idx-32)


def track_from_cat(cat, idx):
    cupidx = (idx-1) / 4
    trackidx = (idx-1) % 4
    cup = cat[cupidx]
    return (cup['tracks'][trackidx], cup['cup'])


def with_numbers(l):
    return zip(range(1, len(l)+1), l)


def tracks_to_list(tracks):
    news = cat_to_list(tracks['new'])
    retros = cat_to_list(tracks['retro'])
    dlcs = cat_to_list(tracks['dlc'])
    return news + retros + dlcs


def cat_to_list(cat):
    return [track
            for cup in cat
            for track in cup['tracks']]


def print_track(n, cup, track):
    out = "[{:>2}] {:>13} - {}".format(n, cup, track)
    print(out)


def list_tracks(tracks):
    for n in range(1, NUM_TRACKS+1):
        track, cup = track_from_idx(tracks, n)
        cup = cup + " Cup"

        # Only print cup name once
        if (n-1) % 4 != 0:
            cup = ""

        # Space between cups
        if (n-1) % 4 == 0 and n != 1:
            print("")

        print_track(n, cup, track)


def print_results(tracks, ns):
    for n in ns:
        track, cup = track_from_idx(tracks, n)
        print_track(n, cup, track)


def random_tracks(num, ban):
    ns = [n
          for n in range(1, NUM_TRACKS+1)
          if n not in ban]

    if len(ns) < num:
        raise ValueError("To much ban! Cannot take {} tracks.".format(num))

    trackidxs = []

    for _ in range(0, num):
        idx = randint(0, len(ns)-1)
        n = ns[idx]
        del ns[idx]
        trackidxs.append(n)

    return trackidxs


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="List all tracks",
                        action="store_true")
    parser.add_argument("-n", "--num-tracks", metavar="NUM_TRACKS",
                        help="Number of tracks to generate", default=4,
                        type=int)
    parser.add_argument("-a", "--all", help="Take all available tracks",
                        action="store_true")
    parser.add_argument("banned", metavar="BANNED", nargs='*', type=int)
    return parser.parse_args()


def main():
    args = arg_parser()

    print("Mario Kart 8 Track Randomizer!\n")

    if args.list:
        list_tracks(tracks)
    else:
        ban = args.banned
        num = args.num_tracks
        if args.all:
            num = NUM_TRACKS - len(ban)

        if num > NUM_TRACKS - len(ban):
            print(('Too many banned tracks!'
                   ' Cannot sample {} tracks from {} with {} banned!')
                  .format(num, NUM_TRACKS, len(ban)))
        else:
            ns = random_tracks(num, ban)
            print_results(tracks, ns)


if __name__ == "__main__":
    main()
