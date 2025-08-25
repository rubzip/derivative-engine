# 📘 Derivative Engine

A small symbolic differentiation engine in Python.

The goal was to think and desing an analitical diferenciation library using object oriented programming.

It can parse mathematical expressions, simplify them, and compute their symbolic derivatives.

## OOP Design
### Expression Base Class
At the core of the engine is the abstract class `Expression`, which acts as the interface for every mathematical function that can be differentiated.

* Each `Expression` can hold an `argument`, which is itself another `Expression`. This recursive structure allows expressions to be represented as a *tree*.
For example, the expression `sin(x^2)` is stored as a `Sin` node whose argument is a Power node, which in turn contains a `Variable`.

* Another optional attribute is `derivative_class`, which acts as a **factory function** that instantiates the respective derivative `Expression`.
For example, the `Sin` class is defined as:
```python
class Sin(Expression):
    def __init___(self, argument: Expression):
        super().__init__(argument, derivative_class=lambda arg: Cos(arg))
```

* Defined methods are:

  * `derivative()` → Computes the symbolic derivative of the expression (using the chain rule by default). In some specific cases is overiden (Constant or Variable), in the rest of cases use chain rule
```python
def derivative(self) -> Expression:
    return Product(
        self.argument.derivative(),
        self.derivative_class(self.argument)
    )
```

  * `simplify()` → Applies algebraic simplifications to reduce redundant terms.

  * `__call__(x)` → Evaluates the expression numerically at a given value of `x`.

  * `__str__()` → Returns a human-readable string representation of the expression.

This design makes it easy to extend the system with new functions (trigonometric, hyperbolic, exponential, etc.) by subclassing `Expression` and defining their derivative and simplification rules.

### Conjunction Base Class
`Conjunction` is another base class that inhereits from `Expression`.
While a plain `Expression` has a single argument (or None), a Conjunction holds two sub-expressions: `left` and `right`.

It is defined for binary operators such as **addition**, **subtraction**, **multiplication**, **division**, **power**...
```python
class Conjunction(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    @abstractmethod
    def derivative(self) -> Expression: ...

    @abstractmethod
    def simplify(self) -> Expression: ...
```

### Binary Tree Structure
With this object-oriented architecture, any mathematical expression can be represented as a tree (except for non-commutative ternary operators nor higher order operators):
* Classes inheriting from `Conjunction` (`Sum`, `Subtraction`, `Product`, `Division`, ...) form **binary branches**.
* Classes inheriting directly from `Expression` with one `argument` (`Sin`, `Cos`, `Exponential`, ...) form **unary branches**.
* Classes like `Constant` and `Variable` (which do not contain further arguments) form the **leaves**.

### Basic Implementation
In the file `basic.py`, all the fundamental implementations are defined (in addition to the base classes).


We start with `Constant`, which represents a fixed real number inside an expression:
```python
class Constant(Expression):
    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def derivative(self) -> "Constant":
        return Constant(0)

    def __call__(self, x: float) -> float:
        return self.value

    def __str__(self):
        return str(self.value)
```
Next is `Variable`, which represents the variable `x`. Its derivative is always `1`:
```python
class Variable(Expression):
    def __init__(self):
        super().__init__()

    def derivative(self) -> Constant:
        return Constant(1)

    def __call__(self, x: float) -> float:
        return x
```
This file also defines the binary operators `Sum`, `Subtraction`, `Product`, `Division` , which all inherit from the `Conjunction` base class. Each of them overrides the `derivative()` method with the corresponding differentiation rule. For example, `Sum` is implemented as:
```python
class Sum(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right)

    def derivative(self) -> "Sum":
        return Sum(left=self.left.derivative(), right=self.right.derivative())

    def __call__(self, x: float) -> float:
        return self.left(x) + self.right(x)
```

## Parsing System



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
