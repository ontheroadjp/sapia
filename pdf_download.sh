#!/bin/bash

set -Ceu

SCRIPT_FILE_NAME=$(basename $0)
SCRIPT_NAME=${SCRIPT_FILE_NAME%.*}
SELF=$(cd $(dirname $0); pwd)
LOGGING=false
VERSION="0.1.0"
SEPARATER='---------------------------'

function _usage() {
    echo "Usage: ${SCRIPT_NAME} [OPTIONS] FILE"
    echo "  This is the boilerplate for shell script."
    echo
    echo "Options:"
    echo "  -h, --help                     Show help"
    echo "  -v, --version                  Show script version"
    echo "  -a, --long-a ARG               Option which must have argument"
    echo "  -b, --long-b [ARG]             Either with or without argument is possible"
    echo "  -c, --long-c                   Option without argument"
    echo "      --verbose                  Print various logging information"
    echo
    exit 0
}

function _log() {
    ${LOGGING} && echo "$@" || return 0
}

function _err() {
    echo "${SCRIPT_NAME}: $1" && exit 1
}

function _args_count() {
    echo ${#ARG_VALUES[@]}
}

function _is_exist() {
    [ -f $1 ] || [ -d $1 ] || [[ $(type $1) ]]
}

# -------------------------------------------------------------

ARG_VALUES=()
OPT_A=""
OPT_B=""
IS_FLAG_P=false
IS_FLAG_Z=false

function _verbose() {
    #_log "ARG_VALUES: ${ARG_VALUES[@]}"
    _log "OPT_A: ${OPT_A}"
    _log "OPT_B: ${OPT_B}"
    _log "IS_FLAG_P: ${IS_FLAG_P}"
    _log "${SEPARATER}"
}

function _main() {
    _log "Wellcome to ${SCRIPT_NAME}"
    DIST=${SELF}/downloads
    mkdir -p ${DIST}
    FILE_NAME=${1}
    while read URL
        wget -P ${DIST} ${URL}
    do
    echo "All done."
}

# -------------------------------------------------------------

function _analyse_args_and_options() {
    while (( $# > 0 )); do
        case $1 in
            -h | --help)
                _usage
                exit 1
                ;;
            -v | --version)
                echo ${SCRIPT_NAME} v${VERSION}
                exit 0
                ;;
            --verbose)
                LOGGING=true
                shift
                ;;

            # Must have argument
            -a | --long-a)
                set +u
                if [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
                    _err "-a option requires a value."
                fi
                set -u
                OPT_A=$2
                shift 2
                ;;

            # Either with or without argument is possible
            -b | --long-b)
                set +u
                if [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
                    shift
                else
                    OPT_B=$2
                    shift 2
                fi
                set -u
                ;;

            # no argument
            -c | --long-c)
                shift 1
                ;;

            # after this all args include '-xx', will treat arg value
            -- | -)
                shift 1
                ARG_VALUES+=( "$@" )
                break
                ;;

            # for true or false flags, no argument
            --*)
                if [[ "$1" =~ 'z' ]]; then
                    IS_FLAG_Z='true'
                fi
                shift
                ;;

            # for true or false flags, no argument
            -*)
                if [[ "$1" =~ 'b' ]]; then
                    IS_FLAG_P='true'
                fi
                shift
                ;;

            # arguments
            *)
                ARG_VALUES+=("$1")
                shift
                ;;
        esac
    done
}

function _set_static_var() {
    :
}

function _verify_static_var() {
    :
}

function _err_check() {
    if _args_count == 0 && _err
}

# -------------------------------------------------------------
# Main Routine
# -------------------------------------------------------------
_analyse_args_and_options $@ && {
    _set_static_var && _verify_static_var && {
        _err_check
        _verbose
        _log 'start main process..' && _log "${SEPARATER}"
        _main
    }
}
exit 0
