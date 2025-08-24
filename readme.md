# 📘 Derivative Engine

A small symbolic differentiation engine in Python.
It can parse mathematical expressions, simplify them, and compute their symbolic derivatives.

## 🚀 Installation

Clone the repository and move into the project folder:

```bash
git clone https://github.com/rubzip/derivative-engine.git
cd derivative-engine
pip install pytest
```

Python 3.10+ is required.

## ▶️ Interactive usage

Run the main script:
```bash
python derivative_engine.py
```

This will open an interactive loop. Enter a function in terms of x, and the program will return its simplified derivative.

To exit, type:
```bash
exit()
```

## ✍️ Examples

Input:
```
function to derivate: sin ( x)
cos(x)
function to derivate: cos(x)
-sin(x)
function to derivate: x^2
2 * x
function to derivate: x^2 + 3*x + 5 + exp(x)
2 * x + 3 + exp(x)
```

## 📚 Supported syntax

* Constants and variable:
```1, 2.5, x```

* Basic operators:
```+, -, *, /, ^```

* Trigonometric functions:
```sin(x), cos(x), tan(x)```

* Hyperbolic functions:
```sinh(x), cosh(x), tanh(x)```

* Exponential and logarithm:
```exp(x), ln(x)```

## ⚡ Automatic simplification

The engine applies basic rules such as:

 * `x + 0 → x`  
 * `x - x → 0`  
 * `x * 1 → x`  
 * `(x ^ 1) → x`  
 * `exp(ln(x)) → x`

## 🧪 Tests

For running tests:
```bash
python -m pytest test/ -v
```
