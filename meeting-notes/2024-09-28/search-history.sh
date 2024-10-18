#!/bin/bash

#################################################
# constants:
# (not really, but they're used like constants)
#################################################
INDENT_WIDTH=4
INDENT_CHAR=" "

######################
# utility functions:
######################
repeat_char() {
    local char="$1"
    local count="$2"
    local result=""

    for ((i=0; i<count; i++)); do
        result="${result}${char}"
    done

    echo "$result"
}

function indent () {
    local indent_prefix
    indent_prefix=$(repeat_char "$INDENT_CHAR" "$INDENT_WIDTH")
    sed 's/^/'"$indent_prefix"'/'
}

function print_code() {
    local function_name="$1"
    type "$function_name" | tail --lines=+2 | indent
}

#########################################
# function to stub out history command:
#########################################
function history {
    # temporarily overriding the history command to produce predictable test results
    file=$(dirname "${BASH_SOURCE[0]}")/fake-history.txt
    cat "$file"
}

###############################################
# the three functions we're going to compare:
###############################################
function search-history-bad() {
    # this function assumes that the search_term is always at the beginning of
    # beginning of the history line, so it searches for the search_term plus
    # any characters after it.
    #
    # this will get rid of the history line number, as required but it will not
    # work correctly if the search_term is found in the middle or at the end of
    # the history line. for example, the command 'ls search_string' will be
    # reported as 'search_string' and 'cp search_string /tmp' will be reported
    # as 'search_string /tmp'.
    local search_term="${1}.*"
    history | grep -E --only-matching "$search_term" | head --lines=50
}

function search-history-good {
    # this function will work to find the search string in any position in a history
    # string, and will return the complete history line (not just part of it). it 
    # does this but using the 'cut' command to trim the first 8 characters from each
    # matching line of history.
    #
    # however, this solution seems fragile. if the history command changes the format
    # of its output, this function will break. it would be better to use a more 
    # robust solution.
    local search_term=$1
    history | grep "$search_term" | head --lines=50 | cut --characters=8-
}

function search-history-robust {
    # this solution is more robust than the previous one. it uses the 'awk' command
    # to remove the first field from each line of history. this will work even if the
    # history command changes its output format.
    #
    # in 'awk', the $0 variable represents the entire line, and $1 represents the
    # first field. by setting $1 to an empty string, we effectively remove the first
    # field from each line.
    local search_term=$1
    history | grep "$search_term" | head --lines=50 | awk ' { $1=""; print $0 } '
}

function demo-function {
    function_name="$1"
    echo ""
    echo "About to run '$function_name'. Here is the relevant code:"
    echo ""
    print_code "$function_name"
    echo ""
    echo "Running '$function_name \"name\"'."
    echo ""
    "$function_name" name | indent | head --lines=25
    echo ""
}


# main:
clear
echo ""
echo "$0 starting."
echo ""
echo "This script demonstrates three different ways to search the bash history for a string."
echo ""
echo "The three functions are:"
echo "  - search-history-bad"
echo "  - search-history-good"
echo "  - search-history-robust"
echo ""
echo "The 'search-history-bad' function is the simplest, but it has a bug."
echo "The 'search-history-good' function fixes the bug, but it's fragile."
echo "The 'search-history-robust' function is the best of the three."
echo ""
echo "There are comments in the code of each function that explain how it works, as well as"
echo "the pros and cons of each approach."
echo ""
echo "Let's see them in action. We'll use each to search an emulated bash history for the"
echo "string \"name\"."
echo ""
echo "Finally, while 'search-history-good' and 'search-history-robust' are both correct,"
echo "their output will be slightly different. You should be able to see this when the screen"
echo "clears the 'search-history-good' output and shows the 'search-history-robust' output."
echo "The differences are subtle, but they are there."
echo ""
echo "For "extra credit," can you figure out why the output is slightly different, and which"
echo "method shows the commands in a form closer to what they were originally?"
echo ""
read -rsp $'Press enter to continue...\n'
clear

for function_name in search-history-bad search-history-good search-history-robust; do
    demo-function "$function_name"
    read -rsp $'Press enter to continue...\n'
    clear
done

echo ""
echo ""
echo "$0 terminating."
