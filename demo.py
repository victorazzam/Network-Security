#!/usr/bin/env python3
"""
Basic shell for running commands to test firewalls.
Written for Year 3 NetSec assignment.

Author: Victor Azzam
"""

import readline
from subprocess import Popen

# Constants
FACEBOOK = "31.13.96.0/19,31.13.64.0/18,31.13.24.0/21,185.60.219.0/24,185.60.218.0/24,185.60.217.0/24,185.60.216.0/22"

# Commands to enable tests
tests1 = {
    "ssh_basic" : ["iptables -A INPUT -p tcp --dport 22 -j DROP"],
    "source_ip" : ["iptables -A INPUT -p tcp -s 172.20.10.4 -j DROP"],
    "dest_range" : [f"iptables -A OUTPUT -p tcp -d {FACEBOOK} -j DROP"]
}

# Commands to disable tests
destroy1 = {
    "ssh_basic" : ["iptables -D INPUT 1"],
    "source_ip" : ["iptables -D INPUT 1"],
	"dest_range" : ["iptables -D OUTPUT 1" for x in " "*7]
}

tests2 = {
	"ssh_basic" : ["nft add rule inet filter input tcp dport 22 drop"],
	"source_ip" : ["nft add rule inet filter input tcp saddr 172.20.10.4 drop"],
	"dest_range" : [f"nft add rule inet filter output tcp saddr {{ {FACEBOOK} }} drop"]
}

destroy2 = {
	"ssh_basic" : ["nft delete rule inet filter input handle 0"],
	"source_ip" : ["nft delete rule inet filter input handle 0"],
	"dest_range" : [f"nft delete rule inet filter output tcp saddr {{ {FACEBOOK} }} drop"]
}

# Tab completion functionality
def complete(text, state):
	for cmd in tests:
		if cmd.startswith(text):
			if not state:
				return cmd
			state -= 1

# Set tab completion function
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

# Configure tests
enabled = set()
green = "\033[92;1m"
tests, destroy = tests1, destroy1

# Disable any active tests
def disable():
	for test in enabled:
		for cmd in destroy[test]:
			Popen(cmd.split(), stdout=open("/dev/null", "w"))

def switch():
	return ((tests1, destroy1), (tests2, destroy2))[(tests, destroy) == (tests1, destroy1)]

while 1:
	try:
		# Clear screen and print menu
		print("\033[1J\033[H", end="")
		print("Test{0}Command(s)\n----{0}----------\n".format(" " * 12), end="")
		for n, t in tests.items():
			c = green * (n in enabled)
			print(f"{n:<16}" + f"\n{'':16}".join(f"{c}{x}\033[m" for x in t))

		# Read user input to toggle tests
		ui = input("\nTest: ").strip()
		if ui[0] == ".":
			disable()
			tests, destroy = switch()
		elif ui in tests:
			if ui in enabled:
				enabled.remove(ui)
				action = destroy
			else:
				enabled.add(ui)
				action = tests
			for cmd in action[ui]:
				Popen(cmd.split(), stdout=open("/dev/null", "w"))

	# Catch SIGINT (Ctrl-C) or EOF (Ctrl-D)
	except (KeyboardInterrupt, EOFError):
		disable() # Clean up before exiting
		exit("")
