#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_URL="https://github.com/onesign12/kbpublisher-community.git"
UPSTREAM_BRANCH="github"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"

if [[ -z "$ROOT" ]]; then
    echo "ERRO: execute dentro de um clone Git do KBpublicar." >&2
    exit 2
fi

cd "$ROOT"

if git remote get-url upstream >/dev/null 2>&1; then
    current="$(git remote get-url upstream)"
    if [[ "$current" != "$UPSTREAM_URL" ]]; then
        echo "Atualizando remote upstream: $current -> $UPSTREAM_URL"
        git remote set-url upstream "$UPSTREAM_URL"
    fi
else
    echo "Adicionando remote upstream."
    git remote add upstream "$UPSTREAM_URL"
fi

echo "Buscando upstream/$UPSTREAM_BRANCH..."
git fetch upstream "$UPSTREAM_BRANCH"

if [[ -f UPSTREAM_BASE ]]; then
    base="$(tr -d '[:space:]' < UPSTREAM_BASE)"
    echo
    echo "Baseline auditado: $base"
    echo "Head upstream:     $(git rev-parse upstream/$UPSTREAM_BRANCH)"
    echo
    if git cat-file -e "$base^{commit}" 2>/dev/null; then
        echo "Commits upstream posteriores ao baseline:"
        git log --oneline "$base..upstream/$UPSTREAM_BRANCH" || true
    else
        echo "AVISO: o commit baseline ainda não existe neste clone."
        echo "       Rode: git fetch upstream $UPSTREAM_BRANCH"
    fi
fi
