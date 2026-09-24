#!/usr/bin/env bash
# Run a shell command on the shop host via SSM, wait, print its output.
#   ssm-run.sh <instance-id> "<command>"
set -euo pipefail
host=$1 cmd=$2
params=$(jq -nc --arg c "$cmd" '{commands: [$c]}')
id=$(aws ssm send-command --instance-ids "$host" --document-name AWS-RunShellScript \
  --parameters "$params" --query Command.CommandId --output text)
for _ in $(seq 180); do
  status=$(aws ssm get-command-invocation --command-id "$id" --instance-id "$host" \
    --query Status --output text 2>/dev/null || echo Pending)
  case $status in Pending|InProgress|Delayed) sleep 5 ;; *) break ;; esac
done
aws ssm get-command-invocation --command-id "$id" --instance-id "$host" \
  --query '[StandardOutputContent,StandardErrorContent]' --output text
[ "$status" = Success ]
