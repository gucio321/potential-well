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

# Math

## Schrödinger equation

After solving the Schrödinger equation for a particle in finite potential well, we get the following solutions:

$$
\psi(x) = \begin{cases}
A\sin(kx) + B\cos(kx) & \text{for } x < 0 \\
C\exp(\alpha x) & \text{for } 0 \leq x \leq L \\
D\exp(-\alpha(x - L)) & \text{for } x > a
\end{cases}
$$

where

$$
k = \sqrt{\frac{2mE}{\hbar^2}}
$$

$$
\alpha = \sqrt{\frac{2m(V - E)}{\hbar^2}}
$$

After applying boundry conditions, we get the following coefficients conditions:

$$
B = C \\
$$

$$
A = \frac{\alpha}{k} B \\
$$

$$
D = B(\frac{\alpha}{k} \sin(kL) + \cos(kL)) \\
$$

$$
-\alpha D = B* k* (\frac{\alpha}{k} \cos(kL) - \sin(kL)) \\
$$

As you can see it is impossible to calculate all parameters. The last condition is the normalization condition:

$$
\int_{-\infty}^{\infty} |\psi(x)|^2 dx = 1
$$

From 2 last conditions we can get transcendental equation for:

$$
\left(\frac{k}{\alpha} - \frac{\alpha}{k}\right) - 2 \frac{1}{\tan(kL)} = 0
$$

We solve this numerically.

## walls height

We need max Psi value (e.g. for wall width):

$$
f(x) = A \sin(kx) + B \cos(kx) \\
$$

$$
f'(x) = k(A \cos(kx) - B \sin(kx)) = 0 \\
$$

$$
\tan(kx) = \frac{A}{B} \\
$$

$$
x = \frac{\arctan(A/B)}{k} \\
$$

$$
x = \frac{\arctan(\alpha/k)}{k} \\
$$

# Motivation

This is a project for Python Lab https://sylabusy.agh.edu.pl/pl/document/8cdc4249-ac97-43c9-b0f7-ea2abdeb50a9.html.
Coop with [@michal1563](https://github.com/michal1563).

# References

- Dear PyGui documentation: https://dearpygui.readthedocs.io/en/latest/reference/dearpygui.html
- Rejection sampling: https://youtu.be/kYWHfgkRc9s
