# Functions I add to .zshrc/.bashrc

My list of modifications/shortcuts/functions/additions I add to all my installations.

| Function / Alias | What it does |
|:--|:--|
| [`hint`](#hint) | Displays a pretty reminder of my custom shortcuts
| [`gitssh`](#gitssh---github-ssh-authentication) | Automates SSH authentication to GitHub
| [`makevenv <path>`](#makevenv-path---python-virtual-environment-creation) | Quickly create a python virtual environment
| [`here`](#here-and-back---marking--returning-to-a-directory) and [`back`](#here-and-back---marking--returning-to-a-directory) | Mark a folder and easily return to it later.

***

## `hint`
I create a lot of alias', some of which are temporary while I am working on a certain project or developing a course.  I found that I would forget them so I made a `hint` function to remind myself.  Every time I open a shell I get a reminder that I can type `hint` to get a list of my custom alias` and/or variables.

Here is an example you add to `.bashrc` or `.zshrc`:

```bash
echo "Enter 'hint' for shortcuts reminder"
function hint() {
    cat << 'EOF'
-----------------------------------------------------------
 p or python      - python3
 makevenv <path>  - Create virtualenv, tempdir if no <path>
 c                - Clear terminal window
 gitssh           - Load git ssh-agent, authenticate
 here / back      - Mark & return to dir
-----------------------------------------------------------
 courses          - Go to Courseware
 projects         - Go to Projects
-----------------------------------------------------------
EOF
}
courses=/Users/myuser/courseware
projects=/Users/myuser/projects
alias python=python3
alias p=python3
alias c=clear
alias courses="cd $courses"
alias projects="cd $projects"
```

### Usage

```bash
hint
```

***

## `gitssh` - GitHub SSH Authentication

I use this `gitssh` function as part of my `.zshrc` to simplify authenticating to GitHub.  

> Edit the `github_ssh_key` variable with your GitHub key name.

```bash
gitssh() {
    local github_ssh_key="github"

    if [[ ! -f ~/.ssh/"$github_ssh_key" ]]; then
        printf "%s\n" "⚠️  No SSH key named '$github_ssh_key' found." "Cannot authenticate to GitHub without SSH key." >&2
        return 1
    fi

    eval "$(ssh-agent)" >/dev/null
    ssh-add ~/.ssh/"$github_ssh_key" >/dev/null

    if ! ssh -T git@github.com 2>&1 | grep -q "You've successfully authenticated"; then
        printf "%s\n" "❌  GitHub Authentication: Failed." >&2
        return 1
    else
        printf "%s\n" "✅  GitHub Authentication: Success." >&2
    fi
}
```

### Usage

```bash
gitssh
```

***

## `makevenv <path>` - Python Virtual Environment Creation

These two functions allow quick creation of a python3 virtual environment.  If you run `makevenv <path>`, where `<path>` is a folder name for your venv, it will create a venv in that folder, ask you if want to install any python packages and then start a python REPL.  Packages to install are entered as a space-separated list.

If you don't specify a `<path>` a venv will be created in the `/tmp` folder.

Add the following to your `.zshrc` (MacOS or Linux) or `.bashrc` (Linux only).

> Note: bash on MacOS will not run this correctly.  Use zsh instead.

```bash
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
```

### Usage

```bash
# Create a folder named project-x and a venv inside it
makevenv project-x

# or 

# Create a venv in /tmp
makevenv
```

***

## `here` and `back` - Marking & Returning to a Directory

Using `cd -` will take you back to your previous directory but it is limited to a single step back.  I use `here` to mark a folder I know I will be coming back to and `back` to take myself back there.  This allows me to move to a variety of folders after marking with `here` and then, when I'm ready to go back to that folder, I need only type `back`.

```bash
here() {
  MARK_DIR="$PWD"
  echo "Directory marked: $MARK_DIR"
}

back() {
  if [ -z "$MARK_DIR" ]; then
    echo "No directory marked."
  else
    cd "$MARK_DIR" || return
  fi
}
```

### Usage

```bash
# mark a folder
here

# Return to the marked folder
back
```

***
