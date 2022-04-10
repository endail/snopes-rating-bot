
# script to make sure $PYTHONPATH is properly set
# run this script every time

PROJECT_DIR="$HOME/$APP_NAME";
LOCAL_SP="$PROJECT_DIR/site-packages";

if ! $(grep -q PYTHONPATH ~/.profile); then
    echo "export PYTHONPATH=$LOCAL_SP" >> ~/.profile;
    source ~/.profile;
fi
