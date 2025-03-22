#!/bin/bash

function test_bashunit_is_working() {
  assert_same "bashunit is working" "bashunit is working"
}

function test_no_its_not() {
  assert_equals "yes it is" "yes it is"
}

