if [ ! -f ".updated" ]; then

  pip install --upgrade pip;
  poetry install --no-root --no-dev --remove-untracked;

  touch .updated;

  git add -A;
  git rm .updated;
  git diff-index --quiet HEAD || git commit -am 'install packages';

fi
