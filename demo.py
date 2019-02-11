from subprocess import Popen

tests = {
    # Basic allow/deny
    "ftp_basic" : "iptables -{} INPUT -p tcp -j DROP --dport 21",
    "ssh_basic" : "iptables -{} INPUT -p tcp -j DROP --dport 22",
    "http" : "iptables -{} INPUT -p tcp -j DROP --dport 80",
    "https" : "iptables -{} INPUT -p tcp -j DROP --dport 443",

    # Custom chains
    "chain_add" : "",
}

enabled = set()
green = "\033[92m"

try:
	while 1:
		print("\033[1J\033[H", end="") # Clear screen
		print("Test{0}Command\n----{0}-------\n".format(" " * 12), end="")
		print("\n".join(f"{n:<16}{green * (n in enabled)}{t.format('A')}\033[m" for n,t in tests.items()))
		ui = input("\nTest: ").strip()
		if ui in tests:
			if ui in enabled:
				enabled.remove(ui)
				action = "D"
			else:
				enabled.add(ui)
				action = "A"
			Popen(tests[ui].format(action).split())
except (KeyboardInterrupt, EOFError):
	print()
