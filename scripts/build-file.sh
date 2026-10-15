#!/usr/bin/env bash
set -euo pipefail

source_file=${1:?Usage: build-file.sh source.c-or-cpp [run]}
action=${2:-build}
project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)

case "$source_file" in
    *.c) compiler=/usr/bin/gcc; standard=c11 ;;
    *.cpp|*.cc|*.cxx) compiler=/usr/bin/g++; standard=c++17 ;;
    *) printf 'Open a .c, .cpp, .cc or .cxx source file first.\n' >&2; exit 2 ;;
esac

file_name=$(basename -- "$source_file")
output="$project_dir/build/active/${file_name%.*}"
mkdir -p -- "$project_dir/build/active"
"$compiler" "-std=$standard" -Wall -Wextra -Wpedantic -g3 -O0 \
    "$source_file" -o "$output"
printf 'Built: %s\n' "$output"

if [[ "$action" == run ]]; then
    exec "$output"
fi
