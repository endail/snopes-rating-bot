
pip install --upgrade pip;
poetry install --no-root;

python -m spacy download en_core_web_sm;

git add -A;
git diff-index --quiet HEAD || git commit -am 'install packages';
