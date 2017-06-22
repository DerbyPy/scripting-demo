import subprocess

# why doesn't this work??
subprocess.run(['dpkg', '-l', 'linux-{image,headers}*'])
