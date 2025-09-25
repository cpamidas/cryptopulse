touch log.txt

generate_commit_message() {
  verbs=("Fix" "Add" "Improve" "Update" "Refactor" "Remove" "Optimize")
  objects=("RPC handler" "CLI argument" "ENS lookup" "token logic" "address parser" "logging" "balance fetch")
  contexts=("flow" "code" "support" "case" "handler" "logic")

  verb=${verbs[$RANDOM % ${#verbs[@]}]}
  object=${objects[$RANDOM % ${#objects[@]}]}
  context=${contexts[$RANDOM % ${#contexts[@]}]}

  echo "$verb $object $context"
}

N=50  # число коммитов

for i in $(seq 1 $N); do
  echo "entry $i" >> log.txt
  git add .

  # равномерное распределение по году
  base_days=$(( (160 / N) * i ))
  random_shift=$((RANDOM % 10 - 5))   # случайный сдвиг ±5 дней
  days=$((base_days + random_shift))
  if [ $days -lt 1 ]; then days=1; fi
  if [ $days -gt 365 ]; then days=365; fi

  # случайное время суток
  hour=$((RANDOM % 24))
  minute=$((RANDOM % 60))
  second=$((RANDOM % 60))

  export GIT_AUTHOR_DATE="$(date -d "$days days ago" "+%Y-%m-%dT%H:%M:%S")"
  export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"

  git commit -m "$(generate_commit_message)"
  git push origin main

  # задержка между 4 и 8 минутами
  sleep $((RANDOM % 241 + 440))
done

