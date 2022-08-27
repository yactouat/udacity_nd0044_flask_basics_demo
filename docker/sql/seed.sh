#!/bin/bash

export PGPASSWORD='pwd'
psql -U 'usr' -d 'todos' -a -f /sql/seed.psql