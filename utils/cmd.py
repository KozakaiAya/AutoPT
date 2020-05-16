import subprocess
import sys
import shlex


def execute(command, working_dir=None):
    if isinstance(command, str):
        command = shlex.split(command)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=working_dir)
    outs, errs = process.communicate()

    outs = outs.decode(sys.stdout.encoding).strip()
    errs = errs.decode(sys.stderr.encoding).strip()
    return outs, errs
