here() {
  MARK_DIR="$PWD"
  echo "Directory marked: $MARK_DIR"
}

back() {
  if [ -z "$MARK_DIR" ]; then
    echo "No directory marked."
  else
    cd "$MARK_DIR" || return
  fi
}