
cd "$HOME/$APP_NAME";

. setenv.bash;

if pgrep -fl "bash update.bash" >/dev/null; then
  # guard against running while updating
  echo "$APP_NAME is updating";
  exit 1;
fi

# if tweepy doesn't exist, determine that to mean
# an update is required
if ! $(python -c "import tweepy" 2>/dev/null); then
  . update.bash;
fi

# check if python main.py is already running
# if not, start it
if ! pgrep -fl "python main.py" >/dev/null; then
  echo "Starting $APP_NAME...";
  poetry run python main.py;
else
  echo "$APP_NAME already running";
fi
