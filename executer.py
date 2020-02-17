import subprocess
import shlex

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            out = output.strip().decode('ascii')
            #print("-----"+out)
        error = process.stderr.readline()
        if error:
            out = error.strip().decode('ascii')
            print("+++++"+out)
    rc = process.poll()
    return rc
    

if __name__ == "__main__":
    run_command("./launch.sh")
    



