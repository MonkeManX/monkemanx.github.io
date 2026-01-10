#!/usr/bin/env bash
# count_words_2025.sh
# Count words in Hugo content files whose front-matter date is in YEAR (default 2025).
# Scans content/{articles,paper-summary,tangled_thoughts}
# Usage:
#   ./count_words_2025.sh [content_dir] [year]
# Example:
#   ./count_words_2025.sh ./content 2025

set -euo pipefail

CONTENT_DIR=${1:-./content}
YEAR=${2:-2025}
SUBFOLDERS=(articles "paper-summary" tangled_thoughts)

if [ ! -d "$CONTENT_DIR" ]; then
  echo "Content directory not found: $CONTENT_DIR" >&2
  exit 1
fi

TOTAL_ALL=0

printf "Counting words for files dated %s in %s\n\n" "$YEAR" "$CONTENT_DIR"

for sub in "${SUBFOLDERS[@]}"; do
  DIR="$CONTENT_DIR/$sub"
  if [ ! -d "$DIR" ]; then
    printf "Skipping missing folder: %s\n\n" "$DIR"
    continue
  fi

  subtotal=0
  printf "Folder: %s\n" "$sub"

  # Use find -print0 + process substitution so the while loop runs in the main shell
  while IFS= read -r -d '' file; do
    # Read first line to detect front-matter type
    firstline=$(head -n 1 "$file" 2>/dev/null || printf "")

    fm=""
    fm_type="none"

    if printf '%s\n' "$firstline" | grep -q '^---'; then
      fm_type="yaml"
      # extract YAML front matter (between first --- and next ---)
      fm=$(awk '
        BEGIN {in_front=0}
        NR==1 { if($0=="---"){ in_front=1; next } else exit }
        in_front==1 {
          if($0=="---"){ exit }
          print
        }
      ' "$file")
    elif printf '%s\n' "$firstline" | grep -q '^\+\+\+'; then
      fm_type="toml"
      fm=$(awk '
        BEGIN {in_front=0}
        NR==1 { if($0=="+++"){ in_front=1; next } else exit }
        in_front==1 {
          if($0=="+++"){ exit }
          print
        }
      ' "$file")
    elif printf '%s\n' "$firstline" | grep -q '^{'; then
      fm_type="json"
      # Best-effort: capture JSON front matter from first "{" to first line starting with "}"
      fm=$(awk '
        BEGIN {in_front=0}
        NR==1 { if($0 ~ /^\{/){ in_front=1; print; next } else exit }
        in_front==1 {
          print
          if($0 ~ /^\}/){ exit }
        }
      ' "$file")
    else
      # no recognized front matter -> skip
      continue
    fi

    # Skip drafts if front matter indicates draft: true / draft = true / "draft": true
    if printf '%s\n' "$fm" | grep -qi -E '^[[:space:]]*draft[[:space:]]*[:=][[:space:]]*true' || \
       printf '%s\n' "$fm" | grep -qi -E '"draft"[[:space:]]*:[[:space:]]*true'; then
      continue
    fi

    # Extract year from date field in front matter.
    # Accepts lines like:
    #   date: 2025-10-13 20:00:00
    #   date: "2025-10-13"
    # If no date found -> skip
    file_year=$(printf '%s\n' "$fm" | grep -Eo 'date[[:space:]]*:[[:space:]]*"?[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -n1 || true)
    if [ -z "$file_year" ]; then
      # Maybe date uses single quotes or more spaces — try more generous match
      file_year=$(printf '%s\n' "$fm" | grep -Eo 'date[[:space:]]*:[[:space:]]*["'\'']?[0-9]{4}-[0-9]{2}-[0-9]{2}["'\'']?' | head -n1 || true)
    fi
    if [ -z "$file_year" ]; then
      continue
    fi
    # Extract the 4-digit year number
    file_year_num=$(printf '%s' "$file_year" | sed -E 's/.*([0-9]{4})-.*/\1/')

    [ "$file_year_num" = "$YEAR" ] || continue

    # Extract body (remove front matter). Handles yaml (---), toml (+++), json ({...}).
    body=$(awk '
      NR==1{
        if($0=="---"){ fm="yaml"; next }
        else if($0=="+++"){ fm="toml"; next }
        else if($0 ~ /^\{/){ fm="json"; next }
        else { fm="none"; print; next }
      }
      {
        if(fm=="yaml" && $0=="---"){ fm=""; next }
        else if(fm=="toml" && $0=="+++"){ fm=""; next }
        else if(fm=="json" && $0 ~ /^\}/){ fm=""; next }
        else if(fm=="" || fm=="none") print
      }
    ' "$file")

    # Clean body:
    # - remove Hugo shortcodes {{< ... >}} and {{% ... %}} (best-effort)
    # - remove HTML tags
    # - convert [text](url) -> text
    # - remove inline backticks
    # - collapse whitespace
    if command -v perl >/dev/null 2>&1; then
      clean=$(printf '%s' "$body" | perl -0777 -pe '
        s/\{\{\s*[%<].*?[%>]\s*\}\}//gs;   # Hugo shortcodes
        s/<[^>]*>//gs;                     # HTML tags
        s/\[([^\]]+)\]\([^\)]+\)/$1/gs;    # Markdown links -> text
        s/`+//gs;                          # remove backticks
        s/^\s+|\s+$//gs;
        s/\s+/ /gs;
      ')
    else
      # sed/awk fallback (less robust but portable)
      clean=$(printf '%s' "$body" | sed -E 's/\{\{\s*[%<][^}]*[%>]\s*\}\}//g; s/<[^>]*>//g; s/\[([^]]+)\]\([^)]*\)/\1/g' | tr -s '[:space:]' ' ')
    fi

    # Count words
    words=$(printf '%s' "$clean" | wc -w | tr -d ' ')

    if [ -n "$words" ] && [ "$words" -gt 0 ] 2>/dev/null; then
      printf "  %6d  %s\n" "$words" "$file"
      subtotal=$((subtotal + words))
    fi

  done < <(find "$DIR" -type f \( -iname '*.md' -o -iname '*.markdown' \) -print0)

  printf "  ------\n  subtotal: %d words\n\n" "$subtotal"
  TOTAL_ALL=$((TOTAL_ALL + subtotal))
done

printf "GRAND TOTAL (%s): %d words\n" "$YEAR" "$TOTAL_ALL"
