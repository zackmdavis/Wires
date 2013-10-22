#!/bin/bash

if [ -f test_database.db ]
    then
    rm test_database.db
    echo "Deleted old test database file"
fi
