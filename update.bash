
# need to delete from replit pip packages

pip install --upgrade pip;
poetry install --no-root;

# download only if not found
#python -m spacy info --silent $APP_SPACY_MODEL || python -m spacy download $APP_SPACY_MODEL;
#python -m spacy info --exclude "spaCy version",Location,Platform,"Python version" | grep $APP_SPACY_MODEL || python -m spacy download $APP_SPACY_MODEL;
#python -m spacy info | grep Pipelines | grep $APP_SPACY_MODEL || python -m spacy download $APP_SPACY_MODEL;

git add -A;
git diff-index --quiet HEAD || git commit -am 'install packages';
