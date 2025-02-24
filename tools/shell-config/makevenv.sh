install_python_requirements() {
    local response requirements_str
    local -a requirements

    printf "❓ Install python requirements (pip)? (y/n):  "
    read -r response

    if [[ $response == "y" ]]; then
        printf "📦 Enter packages as space-separated list:\n"
        read -r requirements_str

        if [[ "$SHELL" == */zsh ]]; then
            requirements=(${=requirements_str})
        else
            IFS=' ' read -r -a requirements <<< "$requirements_str"
        fi

        if (( ${#requirements[@]} > 0 )); then
            printf "Requirements: %s\n" "${requirements[*]}"

            if ! pip install --upgrade pip; then
                printf "❌ Failed to upgrade pip.\n" >&2
                return 1
            fi

            if ! pip install "${requirements[@]}"; then
                printf "❌ Failed to install the specified packages.\n" >&2
                return 1
            fi
        else
            printf "🤷‍♂️ No requirements specified.\n"
        fi
    fi
}

makevenv() {
    local dir venv_dir

    dir="${1:-$(mktemp -d /tmp/python3-XXX)}"
    mkdir -p "$dir"
    venv_dir="$dir/venv"

    printf "🛠️  Creating virtual environment in %s...\n" "$venv_dir"
    if ! python3 -m venv "$venv_dir"; then
        printf "❌ Failed to create virtual environment.\n" >&2
        return 1
    fi

    printf "✅ Activating the virtual environment...\n"
    if ! source "$venv_dir/bin/activate"; then
        printf "❌ Failed to activate the virtual environment.\n" >&2
        return 1
    fi

    install_python_requirements
    python3
}