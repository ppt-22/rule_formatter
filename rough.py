import os

def get_current_shell():
    shell_path = os.environ.get("SHELL")
    print(shell_path)
    if shell_path:
        if "bash" in shell_path:
            return "bashrc"
        elif "zsh" in shell_path:
            return "zshrc"
        else:
            return "Other shell"
    else:
        return "SHELL environment variable not set"

# Example usage:
current_shell = get_current_shell()
print("Current shell:", current_shell)