#!/bin/bash

# This script demonstrates functions and various control structures in Bash.

##################
# shell options:
##################
set -e
set -o pipefail

# if you need to enable step-by-step printing of commands before they execute, uncomment this:
# set -x


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

demo () {
    executable="$1";
    cmdline="$*";
    echo "--------------";
    type "$executable" | indent;
    echo "--------------";
    $cmdline | indent
}


#####################
# sample functions:
#####################
function square_number() {
    local number="$1"
    local result=$((number * number))

    echo $result
    return 0
}

function square_me() {
    # Call the function and capture the returned value
    local number_to_square="$1"
    local squared_value=$(square_number $number_to_square)
    
    # Use the returned value
    echo ""
    echo "The square of $number_to_square is $squared_value."
}


#################
# if statement:
#################
function iffy() {
    local num="$1"

    if [[ $num -eq "0" ]]; then
        echo "\$num is the very special integer 0!"
    elif [[ $num =~ [+-]?[0-9]+ ]]; then
        echo "\$num is $num!, which is a non-zero integer."
    else
        echo "\$num is '$num', which is not an integer."
        echo "Y U NO GIVE ME AN INTEGER?"
        echo "I'm sorry for yelling. I'm just so very passionate about integers."
    fi
}


#############
# for loop:
#############
function globby() {
    local glob="$1"
    
    for f in "$glob"; do
        echo "I found a text file named $f."
    done
}


###############
# while loop:
###############
function countdown() {
    # Initialize the counter
    counter=5
    
    # While loop to count down from 5 to 1
    while [ $counter -gt 0 ]; do
        echo "Countdown: $counter"
        counter=$(($counter - 1))
        sleep 1
    done

    echo "Time's up!"
}


###################
# case statement:
###################
function weekday() {
    # Get the current day of the week
    day=$(date +%A)
    
    # Case statement to print a message based on the day
    case $day in
        "Monday")
            echo "Start of the work week!"
            ;;
        "Tuesday")
            echo "It's Tuesday. Keep going!"
            ;;
        "Wednesday")
            echo "Midweek already!"
            ;;
        "Thursday")
            echo "Almost there!"
            ;;
        "Friday")
            echo "It's Friday! Weekend is near."
            ;;
        "Saturday|Sunday")
            echo "Enjoy your weekend!"
            ;;
        *)
            echo "Unknown day: $day"
            ;;
    esac
}


################
# select loop:
################
function fruit_loop() {
    # Define the options
    PS3="Please select your favorite fruit: "
    options=("Apple" "Banana" "Cherry" "Quit")
    
    # Select loop to display the menu
    select fruit in "${options[@]}"; do
        case $fruit in
            "Apple")
                echo "You selected Apple."
                ;;
            "Banana")
                echo "You selected Banana."
                ;;
            "Cherry")
                echo "You selected Cherry."
                ;;
            "Quit")
                echo "Exiting loop."
                break
                ;;
            *)
                echo "Invalid option. Please try again."
                ;;
        esac
        echo ""
    done
}


##################################################
# "main" function: (this is another select loop)
##################################################
function main() {

    PS3=$'\nWhat code feature do you want to demo? '
    options=("functions" "if statement" "for loop" "while loop" "case statement" "select loop" "quit")

    echo ""        
    select action in "${options[@]}"; do
        echo ""
        echo "You selected $action."
        case $action in 
            "functions")
                echo "About to call the sample function 'square_me 12'. Here is the relevant code."
                echo ""
                print_code square_me
                print_code square_number
                echo ""
                echo "Calling 'square_me 12'."
                square_me 12
                break
                ;;
            "if statement")
                echo "About to call 'iffy' with several different values. Here is the relevant code."
                echo ""
                print_code iffy
                echo ""
                echo "Calling 'iffy 3'."
                iffy 3
                echo ""
                echo "Calling 'iffy +5'."
                iffy +5
                echo ""
                echo "Calling 'iffy -8'."
                iffy -8
                echo ""
                echo "Calling 'iffy 0'."
                iffy 0
                echo ""
                echo "calling 'iffy'."
                iffy
                echo ""
                echo "Calling 'iffy ab'."
                iffy ab
                break
                ;;
            "for loop")
                local tmpdir
                tmpdir=$(mktemp -d)
                echo ""
                echo "Populating temporary directory $tmpdir with 10 *.txt files."
                touch "$tmpdir"/{01..10}.txt
                echo ""
                echo "About to call 'globby \"$tmpdir/*.txt\"'. Here is the relevant code."
                print_code globby
                echo ""
                echo "Calling 'globby ""$tmpdir"/*.txt"'."
                globby "$tmpdir/*.txt"
                echo ""
                echo "Deleting temporary directory $tmpdir."
                rm -rf "$tmpdir".
                break
                ;;
            "while loop")
                echo ""
                echo "About to call 'countdown'. Here is the relevant code."
                echo ""
                print_code countdown
                echo ""
                echo "Calling 'countdown'."
                countdown
                break
                ;;
            "case statement")
                echo "About to call 'weekday'. Here is the relevant code."
                echo ""
                print_code weekday
                echo ""
                echo "Calling 'weekday'."
                weekday
                break
                ;;
            "select loop")
                echo "About to call 'fruit_loop'. Here is the relevant code."
                echo ""
                print_code fruit_loop
                echo ""
                fruit_loop
                break
                ;;
            "quit")
                echo ""
                echo "Option 'quit' selected. Exiting script."
                exit 0
                ;;
            "*")
                echo ""
                echo "$REPLY is an invalid option. Please try again."
                break
                ;;
        esac
    done
}


###################################################################
# call main()
#------------
# this puts the main() function into an infinite loop, so it runs 
# until the user chooses the option to quit.
###################################################################
echo ""
echo "Warning: Portions of this script may interact with the user"
echo "         in mashburger, which may not be suitable Mr. Tice."
echo ""

while true; do
    main
done
