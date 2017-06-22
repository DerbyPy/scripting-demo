import subprocess

# Finally!!
print(subprocess.run(['dpkg', '-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*']))
