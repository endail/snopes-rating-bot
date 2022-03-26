
pip install --upgrade pip;
poetry install --no-root;

git add -A
git diff-index --quiet HEAD || git commit -am 'install packages';
