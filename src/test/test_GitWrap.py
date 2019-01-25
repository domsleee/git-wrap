import src.GitWrap as GitWrap
import os
import shutil

def test_constructor():
  GitWrap.GitWrap('/tmp')

def long_string(s):
  return '\n'.join(s.splitlines())

def test_basics():
  shutil.rmtree('/tmp/GitWrap')
  os.mkdir('/tmp/GitWrap')
  repo = GitWrap.GitWrap('/tmp/GitWrap')
  with open('/tmp/GitWrap/a', 'w') as fout:
    fout.write('hi')
  repo.init()
  repo.add('.')
  stdout = repo.status()

  EXP_STATUS = long_string('''On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

	new file:   a


''')

  print('"'+EXP_STATUS+'"')
  print('"'+stdout+'"')

  assert(stdout == EXP_STATUS)
