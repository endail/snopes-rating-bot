
PROJECT_DIR="$HOME/$APP_NAME";
LOCAL_SP="$PROJECT_DIR/site-packages";
PYTHONPATH="$LOCAL_SP";

cd "$PROJECT_DIR";

# check if python main.py is already running
# if not, start it
if ! pgrep -fl "python main.py" >/dev/null; then
  echo "Starting bot program...";
  poetry run python main.py;
else
  echo "Bot program already running";
fi
