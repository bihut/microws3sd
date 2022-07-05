import sys
import json
import subprocess
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

if (len(sys.argv) !=2):
    exit(-1)
else:
    data = json.loads(sys.argv[1])
    model = data['model']
    animations = data['animations']
    print("model:",model)
    print("animations:",animations,"    ",type(animations))
    textures=""
    try:
        if data['textures'] is not None:
            textures=data['textures']
            print("textures:",textures)
    except KeyError:
        pass

import subprocess
def execute(cmd):
    """
        Purpose  : To execute a command and return exit status
        Argument : cmd - command to execute
        Return   : result, exit_code
    """
    process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (result, error) = process.communicate()
    rc = process.wait()
    if rc != 0:
        print ("Error: failed to execute command: ", cmd)
        print (error.rstrip().decode("utf-8"))
    return result.rstrip().decode("utf-8"), error.rstrip().decode("utf-8")
# def