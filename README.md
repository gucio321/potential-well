# Potential Well Simulator

This programm simulates the movement of a particle in a 1D potential well.

## Installation/setup

You need to have Python 3 installed on your computer.

To set up the project, do the following:

```sh
git clone https://github.com/gucio321/potential-well && cd potential-well
python3 -m virtualenv venv
. venv/bin/activate
python3 -m pip install -r requirements.txt
```

Then to run it, do `python3 main.py`.

# Technologies
- Python 3
- Dear PyGui (Dear ImGui warapper for python)
- GitHub (for version control)
- GitHub Copilot (while codding)

# USP

- The program uses rejection sampling for simulating theoritical particle movement.
- There is a numerical equation solver for the transcendental equation (which cannot be solved analytically).
- We're using Simpson's rule for numerical integration (needed to apply boundry conditions for Schrödinger equation solutions).
- A whole lot of math behind the scenes used to compute SE solutions' constants.

# Motivation

This is a project for Python Lab https://sylabusy.agh.edu.pl/pl/document/8cdc4249-ac97-43c9-b0f7-ea2abdeb50a9.html.
Coop with [@michal1563](https://github.com/michal1563).

# References

- Dear PyGui documentation: https://dearpygui.readthedocs.io/en/latest/reference/dearpygui.html
- Rejection sampling: https://youtu.be/kYWHfgkRc9s
