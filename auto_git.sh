#!/bin/bash

# 🔍 1. Git 프로젝트인지 확인
if [ ! -d ".git" ]; then
  exit 1
fi
# 🔍 현재 폴더명 Vs origin Repo명 확인인
CURRENT_NAME=$(basename "$(pwd)")
ORIGIN_URL=$(git config --get remote.origin.url 2>/dev/null)
REMOTE_NAME=$(basename -s .git "$ORIGIN_URL")

# ✅ 비교
if [ "$CURRENT_NAME" != "$REMOTE_NAME" ]; then
  exit 1
fi

echo "🔍 VSCode 감시 시작 중..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEN_SCRIPT="$SCRIPT_DIR/commit_gen.py"

# 초기 감지 상태 설정
if tasklist | grep -q "Code.exe"; then
  PREVIOUS_RUNNING=1
else
  PREVIOUS_RUNNING=0
fi

while true; do
  if tasklist | grep -q "Code.exe"; then
    if [ "$PREVIOUS_RUNNING" -eq 0 ]; then
      PREVIOUS_RUNNING=1
    fi
  else
    if [ "$PREVIOUS_RUNNING" -eq 1 ]; then
      python "$GEN_SCRIPT"
      PREVIOUS_RUNNING=0
    fi
  fi
  sleep 10
done
