from functools import partial
import subprocess
from src.Sh import Sh
import re

GIT_ARGS = ['git']

class GitWrap:
  def __init__(self, path):
    self._sh = Sh(path)
    self._git_args = GIT_ARGS + ['-C', self._sh.path]

    try:
      self._check_call('which git')
    except subprocess.CalledProcessError:
      raise ValueError('git is not installed on your system')

    # generate methods for all git subprograms.
    def f(subprogram, *args):
      args_arr = list(args)
      return self._check_call(self._git_args + [subprogram] + args_arr)

    self._subprograms = self._get_all_commands()
    for subprogram in self._subprograms:
      setattr(self, subprogram, partial(f, subprogram))
  
  def list_commands(self):
    ''' list all available git commands that can be called
    '''
    return sorted(self._subprograms)

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
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    rc = p.returncode

    if rc != 0:
      sep = '-'*80
      message = (
        "Error code %d on command '%s'\n" % (rc, args)+
        "STDOUT\n%s\n%s" % (sep, stdout)+
        "STDERR\n%s\n%s" % (sep, stderr)
      )
      raise GitException(message)
    else:
      return (stdout, stderr)

  # Sh functions
  def cwd(self):
    return self._sh.cwd()
  
  def cd(self, path):
    self._sh.cd(self, path)


class GitException(Exception):
  pass

# for debugging
if __name__ == '__main__':
  g = GitWrap('/')
  print(g.list_commands())
  stdout, stderr = g.help()
  print(stdout)
