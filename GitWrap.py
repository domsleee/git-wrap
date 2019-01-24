from functools import partial
import subprocess
from Sh import Sh
import re

GIT_ARGS = ['git']

class GitWrap:
  def __init__(self, path):
    self.sh = Sh(path)
    self.git_args = GIT_ARGS + ['--exec-path='+self.sh.path]

    try:
      self._check_call('which git')
    except subprocess.CalledProcessError:
      raise ValueError('git is not installed on your system')

    # generate methods for all git subprograms.
    def f(subprogram, *args):
      args_arr = list(args)
      return self._check_call(GIT_ARGS + [subprogram] + args_arr)

    subprograms = self._get_all_commands()
    for subprogram in subprograms:
      setattr(self, subprogram, partial(f, subprogram))
  
  def _get_all_commands(self):
    stdout, stderr = self._check_call(['git', 'help',  '--all'])
    commands = []
    spl = stdout.split('\n')
    cms = False
    num_spaces = 0
    for line in spl:
      if line.startswith('available git commands in'):
        cms = True
      elif not cms:
        continue
      elif num_spaces >= 2:
        break
      else:
        if line == '':
          num_spaces += 1
        else:
          spll = re.sub(r' +', ' ', line.strip()).split(' ')
          commands = commands + [comm.replace('-', '_') for comm in spll]
    return commands

  def _check_call(self, args):
    if type(args) is list:
      args = subprocess.list2cmdline(args)
    p = subprocess.Popen(
      args,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      shell=True
    )
    stdout, stderr = p.communicate(None)
    rc = p.returncode

    if rc != 0:
      sep = '-'*80
      message = "Error code %d on command '%s'\n\nSTDOUT\n%s\n%s" % (rc, args, sep, stdout)
      raise GitException(message)
    else:
      return (stdout, stderr)

  # Sh functions
  def cwd(self):
    return self.sh.cwd()
  
  def cd(self, path):
    self.sh.cd(self, path)


class GitException(Exception):
  pass

if __name__ == '__main__':
  g = GitEz('/')
  stdout, stderr = g.help()
  print(g.cwd())
  print(stdout)
