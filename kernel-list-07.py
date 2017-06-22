from subprocess import Popen, PIPE


# Get our current kernel version
# $(uname -r | sed -r 's/-[a-z]+//')
args = ['uname', '-r']
uname = Popen(args, stdout=PIPE)

# Trim it down to just the version string
args = ['sed', '-r', 's/-[a-z]+//']
sed = Popen(args, stdin=uname.stdout, stdout=PIPE)

# Python docs say this is necessary for uname process to receive SIGPIPE if sed exits.
uname.stdout.close()
sed_stdout, sed_stderr = sed.communicate()
kernel_version = sed_stdout.decode('utf-8').strip()

print('kernel version:', kernel_version)

# Generate the list of packages
args = ['dpkg', '-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*']
dpkg = Popen(args, stdout=PIPE)

# strip that down to only those that are installed and take the second column
args = ['awk', '/ii/{print $2}']
awk = Popen(args, stdin=dpkg.stdout, stdout=PIPE)

# Feed to grep with a reverse matching, i.e. filter out our current kernel from the list of
# installed packages.
args = ['grep', '-ve', kernel_version]
grep = Popen(args, stdin=awk.stdout, stdout=PIPE)

# Python docs say this is necessary for same reason noted above.
dpkg.stdout.close()
awk.stdout.close()

# Let's go
stdout, stderr = grep.communicate()
print(stdout.decode('utf-8').strip())
