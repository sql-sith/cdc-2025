#!/bin/bash

# Note: with bashunit, as of version 0.18.0,
# you must include the keyword 'function' before
# the test function name, or bashunit will detect
# report each function as having duplicate names,
# and it will report the function name as '{'.

working_dir=$(dirname "${BASH_SOURCE[0]}")

# Import the script to be tested
source "$working_dir/math.sh"

# Test the add function
function test_add() {
  local result=$(add 2 3)
  assert_equals "5" "$result"
}

# Test the subtract function
function test_subtract() {
  local result=$(subtract 5 3)
  assert_equals "2" "$result"
}
