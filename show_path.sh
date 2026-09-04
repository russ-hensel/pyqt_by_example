#!/usr/bin/env bash
#
# show_path.sh -- print $PATH, one directory per line
#
# The script inherits PATH from the terminal that runs it, so what
# you see here is what that terminal would search for a command.
#
#   ./show_path.sh          numbered list, marks dirs that are missing
#   ./show_path.sh -p       plain, one bare directory per line, good for piping
#
# An empty entry in PATH ( "::" or a leading/trailing ":" ) means the
# current directory, so it is called out rather than printed as nothing.

plain=0
if [ "$1" = "-p" ]; then
    plain=1
fi

ix=0

# ${PATH//:/newline} turns every colon into a newline, then we just
# read the lines.  -r leaves backslashes alone, IFS= keeps read from
# trimming spaces in a directory name.
while IFS= read -r dir; do
    ix=$(( ix + 1 ))

    if [ "$plain" -eq 1 ]; then
        echo "$dir"
        continue
    fi

    if [ -z "$dir" ]; then
        note="  <-- empty entry, means the current directory"
    elif [ ! -d "$dir" ]; then
        note="  <-- does not exist"
    elif [ ! -x "$dir" ]; then
        note="  <-- not searchable"
    else
        note=""
    fi

    printf '%2d  %s%s\n' "$ix" "$dir" "$note"

done <<< "${PATH//:/$'\n'}"
