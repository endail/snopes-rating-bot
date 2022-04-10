
if pgrep -fl "[u]pdate.bash" >/dev/null; then
  # guard against multiple update invocations
  echo "$APP_NAME is currently updating";
  exit 1;
fi

PROJECT_DIR="$HOME/$APP_NAME";
LOCAL_SP="$PROJECT_DIR/site-packages";
SYSTEM_SP=$(python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])');

cd "$PROJECT_DIR";

. setenv.bash;

# create a dir for the local packages if not already exists
mkdir -p "$LOCAL_SP";

# clear the system and local python package dirs
rm -rf "$LOCAL_SP"/*;
rm -rf "$SYSTEM_SP"/*;

# make sure at least pip is available
python -m ensurepip;

# redirect python packages to local dir
pip config set global.target "$LOCAL_SP";
pip config set user.target "$LOCAL_SP";
pip config set site.target "$LOCAL_SP";

# reinstall essential packages to local dir
python -m pip install --upgrade --force-reinstall pip setuptools wheel poetry;

# install the project deps
poetry install --no-dev;

# commit all the packages for caching
git add -f site-packages/*;
git diff-index --quiet HEAD || git commit -am "install python packages";

# update details
UPDATE_STR="last_update=$(date +%s), REPL_IMAGE=$REPL_IMAGE, REPL_ID=$REPL_ID, HOSTNAME=$HOSTNAME"
curl "$REPLIT_DB_URL" -d "$UPDATE_STR"
