#! /bin/bash

# Check maestro CLI is present

function check_maestro {
    if test -f "../../../maestro"; then
      echo "maestro CLI ✅"
    else
      echo "maestro CLI not found ❌"
    fi
}