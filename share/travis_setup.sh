#!/bin/bash
set -evx

mkdir ~/.pioncore

# safety check
if [ ! -f ~/.pioncore/.pion.conf ]; then
  cp share/pion.conf.example ~/.pioncore/pion.conf
fi
