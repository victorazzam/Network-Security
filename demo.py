#!/usr/bin/env python3
"""
Basic shell for running commands to test firewalls.
Written for Year 3 NetSec assignment.

Author: Victor Azzam
"""

import sys, readline
from subprocess import Popen

# Commands to enable tests
tests = {
    # Basic allow/deny
    "ftp_basic" : ["iptables -A INPUT -p tcp -j DROP --dport 21"],
    "ssh_basic" : ["iptables -A INPUT -p tcp -j DROP --dport 22"],
    "http" : ["iptables -A INPUT -p tcp -j DROP --dport 80"],

    # Custom chains
    "chain_add" : [
		"echo 123 > /dev/null",
		"echo 456 > /dev/null"
	],
}

# Commands to disable tests
destroy = {
    # Basic allow/deny
    "ftp_basic" : ["iptables -D INPUT -p tcp -j DROP --dport 21"],
    "ssh_basic" : ["iptables -D INPUT -p tcp -j DROP --dport 22"],
    "http" : ["iptables -D INPUT -p tcp -j DROP --dport 80"],

    # Custom chains
	"chain_add" : [
		"echo 123 > /dev/null"
	]
}

tests2 = {
	"name" : ["cmd"],
	"" : [
		"cmd",
		"cmd"
	]
}

destroy2 = {
	"name" : ["cmd"],
	"" : [
		"cmd",
		"cmd"
	]
}

if [sys.argv[1:] + [''])[0] == "nft":
	tests = tests2, destroy2

# Tab completion functionality
def complete(text, state):
	for cmd in tests:
		if cmd.startswith(text):
			if not state:
				return cmd
			else:
				state -= 1

# Set tab completion function
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

# Track enabled tests
enabled = set()
green = "\033[92m"

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
		if ui in tests:
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
		# Disable any active tests and exit
		for test in enabled:
			for cmd in destroy[test]:
				Popen(cmd.split(), stdout=open("/dev/null", "w"))
		exit("")
