# Myriware Scripting Language <MSL>
Welcome to MSL, a unique kind of interface. MSL is a bit of its own programming language--complete with a unique syntax, commands, etc.--, however it still relies on another programming lanuage to run.
## Syntax
MSL follows this kinds of syntax:
  * \<cmd> \<cmd_specs ...>:\<input>
 
where
  * cmd = command or module
  * cmd_specs = the subcommands if the cmd is a module, or the name of a variable
  * input = info to pass onto the command

examples
  * <code>echo:"Hello" # prints "Hello"</code>
  * <code>make variable:"Hello World!"</code> makes a var with name "variable" and value "Hello World!"
  * <code>Extern send:10.0.0.0 200 @variable</code> sends a tcp message to 10.0.0.0 on port 200 with message "Hello World!"

### Data Types
There are a few types of data types in MSL. Each is specified by a different identifier.

#### String
<code>"string"</code>

This is the most basic string. It stores chars in a normal string type. Specified by double qoutes.

#### String (Composite)
<code>\`composite {@string}\`</code>

These string as like regular except that they use backticks [`].

## Commands

### Variables

#### Make

<code>make {name}: {info}</code>
* name = variable name
* info = data-input (see data types)

This function is your basic assign variable info function.
