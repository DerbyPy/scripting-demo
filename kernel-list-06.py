from subprocess import Popen, PIPE

# process chain
args = ['dpkg', '-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*']
dpkg = Popen(args, stdout=PIPE)

args = ['awk', '/ii/{print $2}']
awk = Popen(args, stdin=dpkg.stdout)

# Python docs say this is necessary for dpkg process to receive SIGPIPE if awk exits.
dpkg.stdout.close()

# Let's go
awk.communicate()
