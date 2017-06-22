from plumbum.cmd import uname, sed, dpkg, awk, grep

# Get our current kernel version
# $(uname -r | sed -r 's/-[a-z]+//')
chain = uname['-r'] | sed['-r', 's/-[a-z]+//']
print('chain: ', chain)

kernel_version = chain().strip()

print('kernel version:', kernel_version)

# get & filter package list
chain2 = \
    dpkg['-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*'] \
    | awk['/ii/{print $2}'] \
    | grep['-ve', kernel_version]

packages = chain2().strip()

print(packages)
