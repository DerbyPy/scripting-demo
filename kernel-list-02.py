import subprocess

# why doesn't this work??
subprocess.run('''dpkg -l linux-{kernel,image}-*''', shell=True)
