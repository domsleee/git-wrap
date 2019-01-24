import pytest
import Sh

def test_constructor():
  sh = Sh.Sh('/')

def test_cd():
  sh = Sh.Sh('/')
  sh.cd('hello')

def test_cwd():
  sh = Sh.Sh('/')
  assert sh.cwd() == '/'
  sh.cd('hello')
  assert sh.cwd() == '/hello'
  
