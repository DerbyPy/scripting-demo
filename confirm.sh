confirm () {
    read -r -p "${1:-Are you sure?} [y/N]: " response
    case $response in
        [yY][eE][sS]|[yY])
            true
            ;;
        *)
            false
            ;;
    esac
}
if confirm "Something?"; then
    echo 'yes'
else
    echo 'no'
fi
