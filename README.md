# raritan-lupload

A Python 3 utility to upload a Lua script to a Raritan intelligent PDU.

## Requirements

You will need:

+ A Python 3 interpreter/environment installed
+ The Raritan JSON-RPC SDK installed and listed in the `PYTHONPATH` environment varibale
+ A Lua script to upload to your PDU

## Quick start

Open a command prompt.

Set the `UPASS` environment variable to the password of the `admin` user.

Copy the `lupload.py` Python 3 program to the same directory as the Lua script
you want to upload.

Change to that directory in the command prompt.

Type a command line similar to:

```
python lupload.py px3rack monitor-current.lua
```

where `px3rack` is the name of the PDU (you can also specify the IP address instead) and
`monitor-current.lua` is the name of the Lua script you want to upload.

If everything works a message similar to:

```
Upload of Lua script "monitor-current" to PDU px3rack successful
```

If there was a problem an error message will be displayed.

## Script output buffer gets cleared after successful upload

After the successful upload of a script any output in the script output buffer
for that script on the PDU is cleared. This is so the updated script has a fresh start
when it is next run.

## Command line options

There are a few command line options that can be specified.

### Command line option `--user`

By default the `lupload.py` program will log in to the PDU as user `admin`. To specify
a different username use the `--user` command line option. For example:

```
python lupload.py --user andyc px3rack monitor-current.lua
```

will login as the user `andyc`.

### Command line option `--upass`

By default the `lupload.py` program will look for an enviornment variable called `UPASS`
and use the value of it as the password to log into the PDU. If the password is held
in a different environment variable then the name can be specified with the
`--upass` command line option. For example:

```
python lupload.py --upass RARITANPASS px3rack monitor-current.lua
```

will get the password from the environment variable `RARITANPASS`.

### Command line option `--timeout`

By default the `lupload.py` program will wait for up to 10 seconds for a response from
the PDU before giving up with an error messahe. If you want the program to
wait for a longer or shorter time use the `--timeout` command line option.  For
example:

```
python lupload.py --timeout 20 px3rack monitor-current.lua
```

will make the program wait up to 20 seconds before issuing an error message.

## Lua script naming conventions

Lua scripts should have an file suffix (extension) of `.lua` in either upper or lower case.
The main part of the filename should begin with a letter (upper or lowercase) and remaining
letters should be either a letter, a digit, the minus sign (-) or the underscore (_).

Once successfully uploaded the name of the script on the PDU will be the file name
without the `.lua` suffix.

## Scripts overwritten without warning

Beware that if a PDU already contains a script with the same name it will be
overwritten without warning. This seems dangerous but bear in mind that the primary
use of the `lupload.py` program is to upload subsequent revisions of the same
script while it is being developed. Having a `Are you sure (yes/np)` style prompt
on every upload would soon become annoying.

## The autoStart and autoRestart options

Lua scripts on the PDU can be set to start automatically when the PDU initially boots
or is reset. They can also be set to restart should they exit for any reason. On the PDU
this is specified by ticking the boxes next to the following options:

```
[ ] Start automatically at system boot
[ ] Restart after termination
```

on the `Edit Script` page.

By default when the `lupload.py` program uploads a Lua script these options will be
unticked/blank even if they were previously ticked/set. If a script needs one or both
of these options set then put either or both of the following comment lines near the
top of the Lua script:

```
-- autoStart:=yes
```

```
-- autoRestart:=yes
```

Note: the above comments must exactly for this to feature work.

## Default arguments

If the script requires one or more default arguments specified then this is possible
by adding specially formatted comments at the beginning of the script. For example
to add a default argument called `duration` with a value of `60` add the following
comment at the begining of the script:

```
-- defaultArg duration "60"
```

Note that the value must enclosed in double quotes. If the value itself needs to
contain a double quote just include it. For example:

```
-- defaultArg quote """
```

will set the value `quote` to the single character `"`.

## To Do

Here are some of the things that would be good to add to the `lupload.py` program:

+ Put a comment at the begining of the uploaded script with upload details (date, time, user)


----------------------------------------------------------------------

End of README.md
