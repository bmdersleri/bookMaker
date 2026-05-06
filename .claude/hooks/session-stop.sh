#!/bin/bash
# Stop hook — updates SESSION.md timestamp

SESSION_FILE="D:/bookMaker_Deepseek/SESSION.md"
DATE=$(date "+%Y-%m-%d %H:%M")

if [ -f "$SESSION_FILE" ]; then
    # Update the "Son Oturum" line
    sed -i "s/Son Oturum.*/Son Oturum      : $DATE — Devam ediyor/" "$SESSION_FILE" 2>/dev/null || true
    echo "  SESSION.md guncellendi: $DATE" >&2
fi

exit 0
