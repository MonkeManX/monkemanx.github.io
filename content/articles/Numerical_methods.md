---
title: 'Numerical Methods for Computer Scientist'
date: 2025-07-15 09:00:00
tags: ["Mathematics"]
draft: True
---

The following is a sheet of numerical problems and their solutions. It is a mix of problems taken from old exams and practice sheets from the [KIT](https://www.kit.edu/english/) *"[Numerische Mathematik für die Fachrichtungen Informatik](https://www.math.kit.edu/ianm3/edu/numinfing2022s/de)"* lecture.
This is similar to the article [Optimization Problem](/articles/optimization_problems/), but for numerical problems instead.

## Problems with Confirmed Solution

This section contains only problems with official solutions.

### Problem 1: Floating Point Arithmetic

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
e_{max} &= e_{min} + \sum_{i = 0}^{L_e -1 } (B-1) B^l \\
&= e_{min} + (B-1) \sum_{i = 0}^{L_e -1 } B^l \\
&= e_{min} + (B-1) \frac{1-B^L_e}{1 - B} \\
&= e_{min} - (B-1) \frac{1-B^L_e}{B - 1} \\
&= e_{min} - (1-B^L_e) \\
&= e_{min} + B^{L_e} - 1
\end{align*}
$$

(ii)
$$
\begin{align*}
|m| &= |\sum_{l = 1}^{M} a_l B^{-l}| \\
&\geq | 1 \cdot B^{-1}| \\
&\geq B^{-1} \\
\\
|m| &= |\sum_{l = 1}^{M} a_l B^{-l}| \\
&\leq (B -1 ) \sum_{l = 1}^{M} B^{-l} \\
&= (B -1 ) \sum_{l = 0}^{M-1} B^{-1} B^{-l} \\
&= (B - 1) (B^{-1}) \frac{1 - B^{-M}}{1 - B} \\
&= (B - 1) (B^{-1}) \frac{1 - B^{-M}}{-(B-1)} \\
&= \frac{1 - B^{-M}}{-B} \\
&\leq 1
\end{align*}
$$

(iii)
$$
\begin{align*}
-minFL = maxFL =^{(ii)} B^{E^+}(B^{-M} - 1)
\end{align*}
$$


(iv)
$$
\begin{align*}
minFL_+ = B^{e_{min}}B^{-1} = B^{e_{min} - 1}
\end{align*}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}
For `eps` we have:
$$
eps = \frac{B^{1-M}}{2}
$$

For single precision:
- \(E^+ = -126 + 2^8 -1 = 129\)
- \(maxFL = 2^{129}(1 - 2^{-52}) = 6.8 * 10^{38}\)
- \(minFL_+ = 2^{-126 -1} = 5.8 * 10^{-39}\)
- \(eps = 1.10 * 10^{-7}\)

For double precision:
- \(E^+ = 1025\)
- \(maxFL = 3.6 * 10^{308}\)
- \(minFL_+ = 1.1* 10^{-308}\)
- \(eps = 2.2 * 10^{-16}\)

{{< /details >}}



{{< details "Solution c)" "false" >}}

$$
\begin{align}
f(x) &= \sqrt{x + \frac{1}{x}} - \sqrt{x - \frac{1}{x}} \\
     &= \left(\sqrt{x + \frac{1}{x}} - \sqrt{x - \frac{1}{x}}\right)
         \frac{\sqrt{x + \frac{1}{x}} + \sqrt{x - \frac{1}{x}}}
              {\sqrt{x + \frac{1}{x}} + \sqrt{x - \frac{1}{x}}} \\
    &= \frac{2}{x(\sqrt{x + \frac{1}{x}}) + \sqrt{x + \frac{1}{x}})} \\
    &= \hat{f}(x)
\end{align}
$$

We can then calculate the derivative of \(f(x)\) and \(\hat{f}(x)\) the absolute condition number is then the absolute value of the derivative.

$$
|f'(100)| = 0.000015 = |\hat{f}(100)|
$$


{{< /details >}}



### Problem 2: LR-Decomposition

Let \(\alpha \in \mathbb{R} \setminus \{0\}\), \(\beta, \gamma, \delta \in \mathbb{R}\) and

$$
A = \begin{pmatrix} \alpha & \beta \\ \gamma & \delta \end{pmatrix}.
$$

a) Derive the LR-decomposition \(A = LR\).

Now let specifically \(\alpha > 0\), \(\beta = \gamma = 1\) and \(\delta = 0\).

b) Determine the condition of \(A, L\) and \(R\) with respect to \(\| \cdot \|_1, \| \cdot \|_\infty\) and \(\| \cdot \|_F\) as an estimate of the spectral norm.

c) Compare how, for an arbitrary right-hand side \(\mathbf{b} \in \mathbb{R}^2\) and \(|\alpha| \ll 1\), the solutions of the equations

$$
A\mathbf{x}^1 = \mathbf{b}, \quad L R \mathbf{x}^2 = \mathbf{b}
$$

react to a relative perturbation of the right-hand side of 10%.


{{< details "Solution a)" "false" >}}

We want to find a matrix \(R\) and \(L\) so that

$$
A = LR
$$

with

$$
L = \begin{pmatrix} 1 & 0 \\ l_{21} & 1 \end{pmatrix} \quad
R = \begin{pmatrix} r_{11} & r_{12} \\  0 & r_{22} \end{pmatrix}
$$

Thus we get:

$$
\begin{align}
\alpha &= r_{11} \\
\beta &= r_{12} \\
\gamma &= l_{21} r_{11} \\
\delta &= l_{21} r_{12} + r_{22}
\end{align}
$$

which is the same as:

$$
\begin{align}
\alpha &= r_{11} \\
\beta &= r_{12} \\
\gamma &= l_{21} \alpha \\
\delta &= l_{21} \beta + r_{22}
\end{align}
$$

Hence

$$
\begin{align}
\alpha &= r_{11} \\
\beta &= r_{12} \\
l_{21} &= \frac{\gamma}{\alpha} \\
r_{22} &= \delta - l_{21}\beta = \delta - \frac{\gamma\beta}{\alpha}
\end{align}
$$

So our final decomposition is

$$
L = \begin{pmatrix} 1 & 0 \\ \frac{\gamma}{\alpha} & 1 \end{pmatrix} \quad
R = \begin{pmatrix} \alpha & \beta \\ 0 & \delta - \frac{\gamma\beta}{\alpha}
 \end{pmatrix}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

We calculate the condition number as follows

$$
cond(A) := ||A||||A^{-1}||
$$

Thus we first calculate the inverse. In generals if we have a matrix \(B\)
$$
B = \begin{pmatrix} a & b \\  c & d \end{pmatrix}
$$


Then the inverse \(B^{-1}\) is calculated with

$$
B^{-1} = \frac{1}{ad-bc} \begin{pmatrix} d & -b \\  -c & a \end{pmatrix}
$$

Hence

$$
A^{-1} = \begin{pmatrix} 0 & -1 \\ -1 & \alpha \end{pmatrix} \quad
L^{-1} = \begin{pmatrix} 1 & 0 \\ -\frac{1}{\alpha} & 1 \end{pmatrix} \quad
R^{-1} = \begin{pmatrix} -\frac{1}{\alpha} & -1 \\ 0 & \alpha \end{pmatrix}
$$

Thus

$$
\begin{align}
cond_F(A) &= ||A||_F \cdot ||A^{-1}||_F = \sqrt{2 + \alpha} \cdot \sqrt{2 + \alpha} = 2 + \alpha \\
cond_1(A) &= ||A||_F \cdot ||A^{-1}||_F = (1 + \alpha) \cdot (1 + \alpha) = (1 +  \alpha)^2 \\
\\
cond_F(L) &= 2 + \frac{1}{\alpha^2}\\
cond_1(L) &= (1 + \frac{1}{\alpha})^2
\\
cond_F(R) &= 1 + \alpha^2 + \frac{1}{\alpha^2}\\
cond_1(R) &= max\{1+\alpha, \frac{1}{\alpha}\} \cdot max\{\alpha, 1+ \frac{1}{\alpha}\}
\end{align}
$$

We get the same results for \(||\cdot||_1\) and \(||\cdot||_\infty\).

{{< /details >}}


{{< details "Solution c)" "false" >}}

We have

$$
\frac{|Ax^1|}{|x^1|} \leq K(A) \frac{|Ab|}{|b|} = K(A) \frac{|Ab|}{0.1}
$$

and

$$
\frac{|Ax^2|}{|x^2|} \leq K(L)K(R) \frac{|Ab|}{0.1}
$$

{{< /details >}}
