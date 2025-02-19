#! /bin/bash

function check_status() {
    if [ $? -ne 0 ]; then
      echo $1
    fi
}

echo "validate 🗒️ agents.yaml"
maestro validate ../../../schemas/agent_schema.json ./agents.yaml
check_status "failed to validate agents.yaml ❌"

echo "validate 🗒️ workflow.yaml"
maestro validate ../../../schemas/workflow_schema.json  ./workflow.yaml
check_status "failed to validate worflow.yaml ❌"

echo "run 🏃🏽‍♂️‍➡️ workflow.yaml"
maestro run --dry-run ./agents.yaml ./workflow.yaml
check_status "failed to run worflow ❌"