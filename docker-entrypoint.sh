#!/bin/bash
python manage.py migrate

declare -a cmds=("python manage.py runbot" "python manage.py runserver 0.0.0.0:8000")
for cmd in "${cmds[@]}"; do {
  echo "Process \"$cmd\" started";
  $cmd & pid=$!
  PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";