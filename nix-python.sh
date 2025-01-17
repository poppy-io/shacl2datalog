#!/bin/sh
# Cheap and nasty workaround to get Pycharm to play nice with Nix until I figure out emacs
exec nix develop --command python "$@"
