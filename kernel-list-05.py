import subprocess

# lets capture the output
args = ['dpkg', '-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*']
result = subprocess.run(args, stdout=subprocess.PIPE)
#print(result)
