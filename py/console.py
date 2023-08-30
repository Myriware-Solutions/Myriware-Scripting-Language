import random
from runline import runline
from lango import lo
from z_tips import Tips
Lang = lo()

def RunConsole():
  #print(Runtime.l()['console']['output']['opening'])
  print(Lang.console.output.opening)
  random_index = random.randint(0, len(Tips) - 1)
  random_tip = Tips[random_index]
  print("    " + random_tip)
  while True:
    inpu = input("> ")
    #if inpu == Runtime.l()['console']['input']['stop']:
    if inpu == Lang.console.input.stop:
      break
    else:
      runline(inpu)