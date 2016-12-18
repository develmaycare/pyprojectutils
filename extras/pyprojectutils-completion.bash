_bumpversion_complete()
{
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   PYPROJECTUTILS_AUTOCOMPLETE=1 $1 ) )
}
complete -F _bumpversion_complete -o default bumpversion bumpversion.py
