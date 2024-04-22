#!/bin/bash
set -e

cat <<- EOF
NOTE: This scrips assumes that you have already added your SSH key to Tour's Gitlab
EOF

base_repo_url="git@gitlab.com:zino.studio/tour"

repos=(
    'tour_gateway'
    'tour_processor'
    'tour_shared'
)

for repo in "${repos[@]}"; do
    git clone "${base_repo_url}/${repo}"
done

PYPI_ADDRESS="${PYPI_ADDRESS}" make build
