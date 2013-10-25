#!/bin/bash

if [ -f database.db ]
    then
    rm database.db
    echo "Deleted old database file"
fi
cat db_setup.sql | sqlite3 database.db
echo "Seeded new database file"