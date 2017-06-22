from sh import uname, sed, dpkg, awk, grep

# Get our current kernel version
# $(uname -r | sed -r 's/-[a-z]+//')

kernel_version = sed(uname('-r'), '-r', 's/-[a-z]+//').strip()

print('kernel version:', kernel_version)

# get & filter package list
packages = \
    grep(
        awk(
            dpkg('-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*', _env={'COLUMNS': '200'}),
            '/ii/{print $2}'
        ),
        '-ve',
        kernel_version
    )

print(packages.strip())
