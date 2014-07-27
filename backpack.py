#!/usr/bin/env python

import argparse
import urllib2
import json

parser = argparse.ArgumentParser(description='View tf2 backpack.')

parser.add_argument("key", help="Steam API key")
parser.add_argument("profile", help="SteamID64" )
parser.add_argument("-d", "--duplicates", help="Show only items when there is more than 1", action="store_true")
parser.add_argument("--debug", action="store_true")

args = parser.parse_args()

if args.debug:

    print "key:", args.key
    print "profile:", args.profile

    if args.duplicates:
        print "Show only dupes"

schema_url = "http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key=" + args.key


print "Downloading item schema..."

schema = json.load(urllib2.urlopen(schema_url))


print "OK"

items_url = "http://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001/?key=" + args.key +"&SteamID=" + args.profile


print "Downloading player items..."

items = json.load(urllib2.urlopen(items_url))

print "OK"
print

items = items["result"]
schema = schema["result"]

item_names = {}

for schema_item in schema["items"]:
    item_names[schema_item["defindex"]] = schema_item["name"]


if args.debug:
    print "Status:", items["status"]
    print "Backpack slots:", items["num_backpack_slots"]

items_list = items["items"]

output_dict = {}

for item in items_list:
    defindex = item["defindex"]
    if args.debug:
        print "ID", item["id"]
        print "defindex", defindex
        print "name", item_names[item["defindex"]]
        print
    if output_dict.has_key(defindex):
        output_dict[defindex] += 1
    else:
        output_dict[defindex] = 1

for defindex, count in output_dict.iteritems():
    if (not args.duplicates) or count > 1:
        print ('{0}: {1}x'.format(item_names[defindex], count))
