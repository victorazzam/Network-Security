import readline
from subprocess import call

tests = {
    # Basic allow/deny
    "ftp_basic" : ["iptables -A INPUT -p tcp -j DROP --dport 21"],
    "ssh_basic" : ["iptables -A INPUT -p tcp -j DROP --dport 22"],
    "http" : ["iptables -A INPUT -p tcp -j DROP --dport 80"],
    "https" : ["iptables -A INPUT -p tcp -j DROP --dport 443"],

    # Custom chains
    "chain_add" : [
		"echo 123 > /dev/null",
		"echo 456 > /dev/null"
	],
}

destroy = {
    "ftp_basic" : ["iptables -D INPUT -p tcp -j DROP --dport 21"],
    "ssh_basic" : ["iptables -D INPUT -p tcp -j DROP --dport 22"],
    "http" : ["iptables -D INPUT -p tcp -j DROP --dport 80"],
    "https" : ["iptables -D INPUT -p tcp -j DROP --dport 443"],
	"chain_add" : [
		"echo 123 > /dev/null"
	]
}

enabled = set()
green = "\033[92m"

try:
	while 1:
		print("\033[1J\033[H", end="") # Clear screen
		print("Test{0}Command\n----{0}-------\n".format(" " * 12), end="")
		for n, t in tests.items():
			c = green * (n in enabled)
			print(f"{n:<16}" + f"\n{'':16}".join(f"{c}{x}\033[m" for x in t))
		ui = input("\nTest: ").strip()
		if ui in tests:
			if ui in enabled:
				enabled.remove(ui)
				action = destroy
			else:
				enabled.add(ui)
				action = tests
			for cmd in action[ui]:
				call(cmd.split())
except (KeyboardInterrupt, EOFError):
	print()
