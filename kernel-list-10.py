from sh import uname, dpkg

# Current kernel version.  You could also get this information by reading from the file
# /proc/sys/kernel/osrelease
uname_output = uname('-r').strip()  # like 4.4.0-79-generic
kernel_version = uname_output.rsplit('-', 1)[0]
print('kernel version:', kernel_version)

packages_output = dpkg('-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*', _env={'COLUMNS': '200'})
packages_list = packages_output.strip().splitlines()

installed_lines = filter(lambda line: line.startswith('ii'), packages_list)
package_names = [line.split()[1] for line in installed_lines]

remove_packages = filter(lambda package: kernel_version not in package, package_names)

print('\n'.join(remove_packages))
