
rm -rf /opt/virtualenvs/python3/lib/python3.8/site-packages/*;

PYTHONPATH=site-packages;

python -m ensurepip;

until poetry install --no-dev
do 
  echo "restarting poetry install";
  sleep 1;
done
