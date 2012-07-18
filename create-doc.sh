
export PYTHONPATH=$PYTHONPATH:${1}
export DJANGO_SETTINGS_MODULE=blackdoveapi.settings
epydoc --html --parse-only --docformat plaintext ${2}
