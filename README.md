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

### Data Types - Single
There are a few types of data types in MSL. Each is specified by a different identifier.

#### String
<code>"string"</code>

This is the most basic string. It stores chars in a normal string type. Specified by double qoutes.

#### String (Composite)
<code>\`composite {@string}\`</code>

These strings can contian variable data, similar to python's <code>f"string"</code>. The variables/functions are stored inside <code>{ brackets }</code>.

#### Number
<code>16</code>

Numbers do not come in different types. They are all floats. This could change in the future, but for now there is only one number.

### Data Types - Composite/Referance

#### Runtime Variable
<code>@Varname</code>

Variables are the way to reuse and recycle data. They can be created in different ways, but they all act the same. Variables are technically not their own type of data; they are only 'placeholders' for them. Their type will be the type of what they referance.

#### Arrays
<code>["Wanna store", "more data?", 16, 32]</code>

Arrays are a great way to combine a bunch of data that you want to loop through later. They can contain any type of Single data or varaible. They cannot house arrays or objects inside themselves (could change)

#### Objects
<code>{ "litterally": "JSON" }</code>

Objects are formed from JSON. They are excatly that, so refferance JSON for objects.

## Commands

### Variables

#### Make

<code>make {name}: {info}</code>
* name = variable name
* info = data-input (see data types)

This function is your basic assign variable info function.

### Break

<code>break {name}</code>
* name = variable name

Removes a variable from the Runtime.
