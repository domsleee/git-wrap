import os

class Sh:
  def __init__(self, path):
    self.path = os.path.join(os.getcwd(), path)
  
  def cd(self, path):
    self.path = os.path.join(self.path, path)
  
  def cwd(self):
    return self.path