PYTHONPATH=site-packages

if ! pgrep -fl 'python main.py' > /dev/null; then
  echo "Starting program"
  poetry run python main.py
else
  echo "Program already running"
fi
