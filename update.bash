
# need to delete from replit pip packages

pip install --upgrade pip;
poetry install --no-root;

# download only if not found
python -m spacy info --silent en_core_web_sm || python -m spacy download en_core_web_sm;

git add -A;
git diff-index --quiet HEAD || git commit -am 'install packages';
