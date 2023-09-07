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

Objects are formed from JSON. They are excatly that, so referance JSON for objects.

#### Tables
Tables are constructed from TableSpeak (Tasp) syntax. This is found [below](#TableSpeak)

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

# TableSpeak
TableSpeak, or Tasp, is an effiecent way to store huge tables of data, and easily change the way that you view it. Let't take an example:

```
=Tasp: # Defines the meta-name of the table. This is used if multiple tables are used within the same file
 <
  (Active=Columns), # Defines which way you are looking at the table
  (Columns=Name&Age) # Defines the Name of the rows
 >

 "Anthony", 16 |
 "John",    17 |
 "Jake",    16 |
 "Jess",    17 |
 "Abidule", 18
;
```

## Meta-name
The meta-name is the name of the table. This can be only word-characters (regex '\w'). When MSL parses Tasp, it stores the name in the Meta attribute of the object. There needs to be an equals sign before the meta-name. This is because Tasp is MSL, meaning that like the string or object, it has a denoter.

## Header
The table Header is all the stuff that falles <code>\< here ></code>. The data entries are in parentisis, and seperated by commas (<code>(...=...), (...=...)</code>). Inside, they contain the tag (left of the equals), and the data (right of the equals). The only accepted values are word-characters and the ampsterstand (&) for defining multiple things.

## Active
The Active tag conatins wich of the following ways the table will be looked at. Columns will look at the vertical strips of data, so all the values fall into one catagory. Rows will look at all the horazontal strips of data, so all the data is connected to each other. If both Columns and Rows are defined, then the return will be a object of objects. The main object will have the keys of the Rows tag. Under that, the secondary object will have keys of the Columns tag and the values of the table's data.

```
# Tasp
=Cols:<(Active=Columns),(Columns=Name&Age&Gender)>
"Anthony", 16, 'm' |
"John",    17, 'm' |
"Jess",    17, 'f' ;

/* Json
{ "Name": [ "Anthony", "John", Jess"],
  "Age": [ 16, 17,  17 ],
  "Gender": [ "m", "m", "f" ] } */

=Rows:<(Active=Rows),(Columns=Anthony&John&Jess)>
16, 'm' |
17, 'm' |
17, 'f' ;

/* Json
{ "Anthony": [16, "m"],
  "John": [17, "m"],
  "Jess": [17, "f"] } */

=Both:<(Active=Columns&Rows),(Columns=Age&Gender),(Rows=Anthony&John&Jess)>
16, 'm' |
17, 'm' |
17, 'f' ;

/*Json
{ "Anthony": {"Age": 16, "Gender": "m"},
  "John": {"Age": 17, "Gender": "m"},
  "Jess": {"Age": 17, "Gender": "f"} } */

```

Tasp is different in the way that you only need a few lines of structure, and then any data you add into it will become large objects of info.

## Data

As you can see, the data entries in the table are that of MSL variables. That does mean that if you use MSL to parse it, functions can be runned. This, however, is a valuability that will be fixed soon. Data can be anything, and it can even be custom classes! The default deliminator is the bar (|), but that can be changed if you use TaspC.

## TaspC

TaspC allowes for even better cross-communications. TaspC stores the header in one file, but the data in another. The 'C' in TaspC is for CSV, as you will soon find out. You can use custom deliminators here, even using return-line (\n). Let's look at an example.

```
ex.tasp
=Cols:<(Active=Columns),(Columns=Name&Age),(TaspC=\n)>"./ex.csv";

ex.csv
 "Anthony", 16
 "John",    17
 "Jake",    16
 "Jess",    17
 "Abidule", 18

