#!/bin/sh

set -e -u

# https://github.com/jinliu/kdotool
kdo() {
    kdotool "$@"
}

# https://github.com/ReimuNotMoe/ydotool
ydo() {
    ydotool "$@"
}

url='https://www.youtube.com/watch?v=3TE5aR7EHus'
p_wclass=org.nickvision.tubeconverter
p_wid="$(kdo search --case-sensitive --class "$p_wclass")"
a_wid="$(kdo getactivewindow)"

echo active "$a_wid"
echo parabolic "$p_wid"

# combine multiple commands into one?
echo switching to parabolic
kdo windowstate --add below "$p_wid"
kdo windowactivate "$p_wid"

echo typing URL into parabolic with newline
printf '%s\n' "$url" | ydo type --key-delay 0 --file -

echo switching back to previous window
kdo windowactivate "$a_wid"
kdo windowstate --remove below "$p_wid"

# gdbus call --session --dest org.nickvision.tubeconverter --object-path /org/nickvision/tubeconverter --method org.freedesktop.Application.Open "['https://www.youtube.com/watch?v=3TE5aR7EHus']" "{}"
# flatpak run org.nickvision.tubeconverter "$url"

# xdg-mime default org.nickvision.tubeconverter.desktop x-scheme-handler/parabolic
# xdg-open 'parabolic://www.youtube.com/watch?v=3TE5aR7EHus'
