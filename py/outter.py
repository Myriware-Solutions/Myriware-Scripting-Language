import tomllib

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Special Colors

Dark_Gray='\033[1;30m'     # Dark Gray

class Outter:
  def out(type, msg):
    f = open("_config.toml", "r")
    c = f.read()
    data = tomllib.loads(c)
    f.close()
    if (data[type]):
      match type:
        case "err":
          print(f"{Red}{msg}{Color_Off}")
        case "pri":
          print(msg)
        case "sec":
          print(f"{Dark_Gray}{msg}{Color_Off}")