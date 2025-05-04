---
title: 'Numerical Methods'
date: 2025-05-04 09:00:00
tags: ["Mathematics"]
draft: True
---


## Solutions Not Checked Yet

### Task 1 (Floating-Point Numbers)

We consider for a given base \( B \geq 2 \), a minimum exponent \( E^{-} \), and lengths \( M \) and \( E \), the finite set of normalized floating-point numbers \(\text{FL}\).

\[
\text{FL} := \left\{ \pm B^e \sum_{l=1}^M a_l B^{-l} : e = E^{-} + \sum_{k=0}^{E-1} c_k B^k, a_l, c_k \in \{0, \ldots, B - 1\}, a_1 \neq 0 \right\} \cup \{0\}
\]

Let \( E^{+} \) be the maximum exponent, \( m \neq 0 \) the mantissa, \( \max \text{FL} \) the largest number of the set, and \( \min \text{FL}_+ \) the smallest positive number of the set.

**a)** Show that:

(i) \( E^+ = E^{-} + B^E - 1 \)  
(ii) \( B^{-1} \leq |m| < 1 \)  
(iii) \( \max \text{FL} = -\min \text{FL} = B^{E^+}(1 - B^{-M}) \)  
(iv) \( \min \text{FL}_+ = B^{E^{-} - 1} \)  

**b)** Calculate for the IEEE Standard of

- **single precision** \((B = 2, E^{-} = -126, M = 23, E = 8)\)
- **double precision** \((B = 2, E^{-} = -1022, M = 52, E = 11)\)

the values for \( E^+ \), \( \max \text{FL} \), \( \min \text{FL}_+ \), and the machine epsilon \( \varepsilon \).

**c)** Reformulate

\[
f(x) = \sqrt{x + \frac{1}{x}} - \sqrt{x - \frac{1}{x}} \quad \text{for } |x| \gg 1
\]

in such a way that cancellation is avoided.  
Determine the absolute condition number of \( f \) at the point \( x = 100 \) before and after the transformation.
**Hint:** *For evaluating the derivatives, we recommend using digital tools.*


{{< details "Solution a)" "false" >}}

(i)
$$
\begin{align*}
E^+ &= \max e \\
&= \max \ B^- + \sum_{k=0}^{E - 1} c_k B^{k} \\
&= B^- + (B - 1) \sum_{k=0}^{E - 1}  B^{k} \\
&= B^- + (B-1) \frac{B^{E - 1} -1}{B -1} \\
&= B^- + B^{E-1} - 1
\end{align*}
$$

(ii)

$$
\begin{align*}
|m| &= |\sum_{l = 1}^{M} a_l B^{-l}| \\
&\leq (B-1) \sum_{l = 1}^{M} B^{-l} \\
&= (B-1) \sum_{l = 0}^{M} B^{-1} B^{-l} \\
&= \frac{(B - 1)}{B} \frac{B^{-M} -1}{B -1} \\
&= B^{-M} - 1 \\
&\leq 1
\end{align*}
$$

and 

$$
|m |= |\sum_{l = 1}^{M} a_l B^{-l}| \geq 1 \cdot B^{-1} = B^{-1}
$$

(iii)

$$
-minFL = maxFL =^{(ii)} B^{E^+}(B^{-M} - 1) 
$$

(iv)
$$
minFL_+ = min{m \cdot B^e} = B^{-1} B^{E^{-}} = B^{E^- - 1}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

*Single Precision:*  
- \(E^+ = -126 + 2^{8} - 1 = 129\)
- \(maxFL = 2^{129}(1 - 2^{-23})\)
- \(minFL_+ = 2^{-126 - 1} = 2^{-127}\)
- \(eps = sup\frac{|x - fl(x)|}{|x|} = ?\)

*Double Precision:*
- \(E^+ = -1022 + 2^{11} - 1 = 1025\)
- \(maxFL = 2^{1025}(1 - 2^{-52})\)
- \(minFL_+ = 2^{-1022 -1 } = B^{-1023}\)
- \(eps = ?\)

{{< /details >}}


{{< details "Solution c)" "false" >}}

Reformulation:

$$
\begin{align*}
f(x)^2 &= (\sqrt{x + \frac{1}{x}} - \sqrt{x - \frac{1}{x}})^2 \\
&= (x + \frac{1}{x}) + (x - \frac{1}{x}) - 2 \sqrt{(x + \frac{1}{x})x - \frac{1}{x}} \\
&= 2x - 2 \sqrt{x^2- (\frac{1}{x})^2}
\end{align*}
$$

Thus 

$$
\hat{f(x)} = \sqrt{2x - 2 \sqrt{x^2- (\frac{1}{x})^2}}
$$

We now calculate the absolute condition number, first we need to claculate the derivatives

$$
\hat{f(x)}' = \frac{2 - \frac{2x + \frac{2}{x^3}}{\sqrt{x^2 - \frac{1}{x^2}}}}{\sqrt{2x - 2 \sqrt{x^2- (\frac{1}{x})^2}}}
$$

$$
f(x)' = \frac{1 - \frac{1}{x^2}}{2 \sqrt{x + \frac{1}{x}}} - \frac{\frac{1}{x^2} + 1}{2\sqrt{x - \frac{1}{x}}}
$$

The absolute condition number is defined as 

$$
K(x) = |\nabla_x f_x k(x)|
$$

This means 

$$
K_{f} = 1.5000000068751684e-05
$$

```py
import math

def f(x):
    numerator1 = 1 - 1 / x**2
    denominator1 = 2 * math.sqrt(x + 1 / x)

    numerator2 = 1 / x**2 + 1
    denominator2 = 2 * math.sqrt(x - 1 / x)

    return (numerator1 / denominator1) - (numerator2 / denominator2)
```


$$
K_{\hat{f}} = -3.000000029963644e-05
$$

```py
import math

def f(x):
    numerator_inner = 2 * x + 2 / x**3
    denominator_inner = math.sqrt(x**2 - 1 / x**2)
    numerator = 2 - (numerator_inner / denominator_inner)
    
    sqrt_inner = math.sqrt(x**2 - (1 / x)**2)
    denominator = math.sqrt(2 * x - 2 * sqrt_inner)
    
    return numerator / denominator
```

{{< /details >}}



### Task2 (LU Decomposition)

Let \(\alpha \in \mathbb{R} \setminus \{0\}\), \(\beta, \gamma, \delta \in \mathbb{R}\), and  

\[
A = \begin{pmatrix}
\alpha & \beta \\
\gamma & \delta
\end{pmatrix}.
\]

**(a)** Derive the LU decomposition \(A = LR\).

Now assume specifically that \(\alpha > 0\), \(\beta = \gamma = 1\), and \(\delta = 0\).

**(b)** Determine the condition number of \(A\), \(L\), and \(R\) with respect to the norms \(\|\cdot\|_1\), \(\|\cdot\|_\infty\), and \(\|\cdot\|_F\) as an estimate of the spectral norm.

**(c)** Compare how, for any arbitrary right-hand side \(b \in \mathbb{R}^2\) and \(|\alpha| \ll 1\), the solutions of the equations  

\[
Ax^1 = b, \quad\quad LRx^2 = b
\]

react to a relative perturbation of the right-hand side of 10%.


{{< details "Solution a)" "false" >}}

$$
A = \begin{pmatrix}
\alpha & \beta \\
\gamma & \delta
\end{pmatrix}
$$

We want to find a matrix \(U\) and \(L\) so that 

$$
A = LU
$$

Hence

$$
L = \begin{pmatrix}
1 & 0 \\
l_{21} & 1
\end{pmatrix}, \quad

U = \begin{pmatrix}
u_{11} & u_{12} \\
0 & u_{22}
\end{pmatrix}
$$

Thus we get 


$$
L = \begin{pmatrix}
1 & 0 \\
\gamma/\alpha & 1
\end{pmatrix}, \quad

U = \begin{pmatrix}
\alpha & \beta \\
0 & \delta - \gamma \beta/ \alpha
\end{pmatrix}
$$

{{< /details >}}

{{< details "Solution b)" "false" >}}

To get the condition we caluclate 

$$
cond(A) = ||A|| \cdot ||A^{-1} ||
$$

Thus for A we get

$$
cond(A)_1 =
cond(A)_\infty =
cond(A)_F =
$$

For L we get 

$$
cond(L)_1 =
cond(L)_\infty =
cond(L)_F =
$$

For U we get

$$
cond(U)_1 =
cond(U)_\infty =
cond(U)_F =
$$

{{< /details >}}

{{< details "Solution c)" "false" >}}

So we have 

$$
\begin{pmatrix}
\alpha & \beta \\
\gamma & \delta
\end{pmatrix}
x^1 = 
\begin{pmatrix}
\b_1 \\
\b_2
\end{pmatrix}
$$
{{< /details >}}
