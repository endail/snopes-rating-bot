
LOCAL_SP="$HOME/snopes-rating-bot/site-packages";
SYSTEM_SP=$(python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')

rm -rf "$LOCAL_SP"/*;
rm -rf "$SYSTEM_SP"/*;

export PYTHONPATH="$LOCAL_SP";

python -m ensurepip;

pip config set global.target "$LOCAL_SP";
pip config set user.target "$LOCAL_SP";
pip config set site.target "$LOCAL_SP";

python -m pip install --upgrade --force-reinstall pip;
python -m pip install --upgrade --force-reinstall setuptools;
python -m pip install --upgrade --force-reinstall poetry;

poetry install --no-dev
#until poetry install --no-dev
#do 
#  echo "restarting poetry install";
#  sleep 1;
#done

git add -A;
git diff-index --quiet HEAD || git commit -am "install packages";
