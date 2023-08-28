# Myriware Scripting Language <MSL>
Welcome to MSL, a unique kind of interface. MSL is a bit of its own programming language--complete with a unique syntax, commands, etc.--, however it still relies on another programming lanuage to run.
## Syntax
MSL follows this kinds of syntax:
  *<cmd> <cmd_specs ...>:<input>
where
  *cmd = command or module
  *cmd_specs = the subcommands if the cmd is a module, or the name of a variable
  *input = info to pass onto the command
examples
  *echo:"Hello" # prints "Hello"
  *make variable:"Hello World!" # makes a var with name "variable" and value "Hello World!"
  *Extern send:10.0.0.0 200 @variable # sends a tcp message to 10.0.0.0 on port 200 with message "Hello World!"
##
