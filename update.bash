
PROJECT_DIR="$HOME/snopes-rating-bot";
LOCAL_SP="$PROJECT_DIR/site-packages";
SYSTEM_SP=$(python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])');

cd "$PROJECT_DIR";

# create a dir for the local packages if not already exists
mkdir -p "$LOCAL_SP";

# clear the system and local python package dirs
rm -rf "$LOCAL_SP"/*;
rm -rf "$SYSTEM_SP"/*;

export PYTHONPATH="$LOCAL_SP";

# make sure at least pip is available
python -m ensurepip;

# redirect python packages to local dir
pip config set global.target "$LOCAL_SP";
pip config set user.target "$LOCAL_SP";
pip config set site.target "$LOCAL_SP";

# reinstall essential packages to local dir
python -m pip install --upgrade --force-reinstall pip;
python -m pip install --upgrade --force-reinstall setuptools;
python -m pip install --upgrade --force-reinstall poetry;

# install the project deps
poetry install --no-dev;

# commit all the packages
git add site-packages/*;
git diff-index --quiet HEAD || git commit -am "install python packages";

# have something here to store when the last update occurred
# and on which repl hostname/id/image/cluster
# perhaps this can be used to detect when an update needs to occur?
