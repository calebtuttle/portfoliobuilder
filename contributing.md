# Contributing to Portfolio Builder
## What is Portfolio Builder?
Portfolio Builder is a tool for creating and maintaining a diversified stock portfolio. Using the [Alpaca API](https://alpaca.markets), it makes the purchase of large quantities of stocks easier. It was originally created to duplicate the functionality of stock-index-based ETFs, but its functionality reaches beyond that of the initial vision: It allows investors to effectively craft their own stock ETFs without paying fees.

## Style Guide
Follow the [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/). 

Use descriptive names, and keep functions short. As a rule of thumb, functions should be between 2 and 100 lines, with most being no more than 20 lines. This helps create self-documenting code and can allow for more modular development.

## How to Contribute
I welcome all contributions. Below is a list of how to report issues and add commands. If you would like to contribute some other way, feel free to raise an issue describing what you want to add.

See [this post](https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/) for a general guide on contributing to an open source project.

### Report Issues
To report issues, use the Issues feature in the GitHub repository.
Use the following template when reporting an issue.

Brief Description

Steps to Reproduce:

1.

2.

Expected behavior:

Actual behavior:

Reproduces how often:

### Add a Command
To create a command, open:
- Create a class in [commands.py](portfoliobuilder/commands.py) with the name of the command.
- Add an 'execute()' method to the class that executes the command.
- Update the help string in the Help class in [commands.py](portfoliobuilder/commands.py) to include the command.
- Add both the command keyword and the class to the command_executables
    dictionary in [run.py](portfoliobuilder/run.py).
- Add an entry in [commands.md](docs/commands.md) with the command name and description.

