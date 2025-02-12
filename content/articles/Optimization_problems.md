---
title: 'More Optimization Problems'
date: 2025-02-10
tags: ["Mathematics"]
---

The following is sheet of more optimization problems and their solutions.



## Problem 1 


Consider the following linear optimization problem:

Minimize  

\[
f(x) = 4x_1 + 12x_2 + 3x_3 - 6x_4, \quad x \in \mathbb{R}^4,
\]

subject to the constraints  

\[
-x_1 + 2x_2 - 5x_3 - 2x_4 \geq 2,
\]

\[
2x_1 + x_2 + 3x_3 - x_4 \geq 1,
\]

\[
x_1, x_2, x_3, x_4 \geq 0.
\]

Formulate the dual problem and determine all solutions of the dual problem graphically.


{{< details "Solution" "false" >}}

We write the problem first in its default form

$$
(P) \quad f(x) \ \ \text{unter} \ \ M 
$$

Where

$$
\begin{align}
& M = \{ \\
& -x_1 + 2x_2 - 5x_3 - 2x_4 - x_5 = 2,  \\
& 2x_1 + x_2 + 3x_3 - x_3 - x_6 = 1 \\
& \}
\end{align}
$$

The dual problem is then

$$
\begin{align}
(D) \quad 
\begin{pmatrix}
2 \\
1 
\end{pmatrix}
\begin{pmatrix}
y_1 & y_2 
\end{pmatrix}
\ \ \text{unter} \ \
\begin{pmatrix}
-1 & 2 \\
2 & 1\\
-5 & 3\\
-2 & -1\\
-1 & 0 \\
0 & -1
\end{pmatrix}
\begin{pmatrix}
y_1 & y_2 
\end{pmatrix}
\leq 
\begin{pmatrix}
4 \\
12 \\
3 \\
-6 \\
0 \\
0
\end{pmatrix}
\end{align}
$$

We draw the condition on paper

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/WS17_task1.jpg">
    <figcaption>
        I have drawn this a bit dirty and hastily, thus the solution looks a bit weird.
    </figcaption>
</figure>
{{< /rawhtml >}}

The solution is the line between (4,4) and (6, 0) with the maxiumum value of 12.

{{< /details >}}



## Problem 2

Determine for \(\beta \geq 2\), and the following sytem the possible solutions

$$
\begin{align}
x_1 + x_2 - 2x_3 &= 1, \\
2x_1 + 3x_2 - 5x_3 &= \beta, \\
2x_2 - 5x_3 \leq 4
\end{align}
$$

For every \(\beta\) name its solution.

{{< details "Solution" "false" >}}

The system has a solution if and only if Phase 1 of the Simplex algorithm provides a solution. To achieve this, we introduce a variable \( x_5 \) for the third condition in order to bring the problem into normal form.

Then, we write our problem as a tableau

$$
\begin{array}{cccccc|c}
x_1 & x_2 & x_3 & x_4 & x_5 & x_6 & b \\
\hline
-3 & -4 & 7 & 0 & 0 & 0 & -1 - \beta \\
\hline
\fbox{1} & 1 & -2 & 1 & 0 & 0 & 1 \\
2 & 3 & -5 & 0 & 1 & 0 & \beta \\
0 & 2 & -5 & 0 & 0 & 1 & 4
\end{array}
$$

The pivot element is in the first row and first column since it has the smallest pivot.

$$
\begin{array}{cccccc|c}
x_1 & x_2 & x_3 & x_4 & x_5 & x_6 & b \\
\hline
0 & -1 & 1 & 3 & 0 & 0 & 2 - \beta \\
\hline
1 & 1 & -2 & 1 & 0 & 0 & 1 \\
0 & 1 & -1 & -2 & 1 & 0 & \beta - 2 \\
0 & 2 & -5 & 0 & 0 & 1 & 4
\end{array}
$$

We now look at the second column.

**Case 1:** \( \beta \geq 3 \)  Then, the pivot is in the first row.

$$
\begin{array}{cccccc|c}
x_1 & x_2 & x_3 & x_4 & x_5 & x_6 & b \\
\hline
0 & -1 & 1 & 3 & 0 & 0 & 2 - \beta \\
\hline
1 & \fbox{1} & -2 & 1 & 0 & 0 & 1 \\
0 & 1 & -1 & -2 & 1 & 0 & \beta - 2 \\
0 & 2 & -5 & 0 & 0 & 1 & 4
\end{array}
$$

Thus we get

$$
\begin{array}{cccccc|c}
x_1 & x_2 & x_3 & x_4 & x_5 & x_6 & b \\
\hline
1 & 0 & -1 & 3 & 0 & 0 & 3 - \beta \\
\hline
1 & 1 & -2 & 1 & 0 & 0 & 1 \\
-1 & 0 & \fbox{1} & -3 & 1 & 0 & \beta - 3 \\
-2 & 0 & -1 & -2 & 0 & 1 & 2
\end{array}
$$

And hence

$$
\begin{array}{cccccc|c}
x_1 & x_2 & x_3 & x_4 & x_5 & x_6 & b \\
\hline
0 & 0 & 0 & 1 & 1 & 0 & 0 \\
\hline
-1 & 1 & 0 & -5 & 2 & 0 & 2\beta-5 \\
-1 & 0 & 1 & -3 & 1 & 0 & \beta - 3 \\
-3 & 0 & 0 & -5 & 1 & 1 & \beta - 1
\end{array}
$$

Thus, we are done and have found a solution with  

\[
x^* = (0, 2\beta -5, \beta -3, 0).
\]

**Case 2:** \( 2 \leq \beta \leq 3 \)  Then, the pivot is in the second row.

$$
\begin{array}{cccccc|c}
x_1 & x_2 & x_3 & x_4 & x_5 & x_6 & b \\
\hline
0 & -1 & 1 & 3 & 0 & 0 & 2 - \beta \\
\hline
1 & 1 & -2 & 1 & 0 & 0 & 1 \\
0 & \fbox{1} & -1 & -2 & 1 & 0 & \beta - 2 \\
0 & 2 & -5 & 0 & 0 & 1 & 4
\end{array}
$$

Hence

$$
\begin{array}{cccccc|c}
x_1 & x_2 & x_3 & x_4 & x_5 & x_6 & b \\
\hline
0 & 0 & 0 & 1 & 1 & 0 & 0 \\
\hline
1 & 0 & -1 & 3 & -1 & 0 & -\beta + 3 \\
0 & \fbox{1} & -1 & -2 & 1 & 0 & \beta - 2 \\
0 & 0 & -3 & 4 & -2 & 1 & -2\beta + 8
\end{array}
$$

And thus, we are done with the solution  

\[
x^* = (-\beta + 3, \beta -2, 0).
\]

{{< /details >}}



## Problem 3

Given the function 

$$
f(x, y) = ax^2 + by^2 - 4xy - 2x + 4y
$$

where \(a,b \in \mathbb{R}\) are parameters.

a) Determine all \(a,b\), so that f is convex.  
b) For which \(a,b\) is \((1, 1)\) a local minima of \(f\).

{{< details "Solution" "false" >}}

**a)**  
First, we determine the Hessian matrix of the function. The first derivative is

$$
\nabla f(x) = (2ax - 4y - 2, \ 2by - 4x + 4)
$$

Thus, the Hessian matrix is

$$
\nabla^2 f = H_f = 
\begin{pmatrix}
2a & -4 \\
-4 & 2b
\end{pmatrix}
$$

We determine whether the matrix is positive semidefinite and for which values by using the minors.

$$
det_1(H_f) = 2a
$$

$$
det_2(H_f) = 4ab - 12
$$

That is, the matrix is semidefinite, and therefore the function \( f \) is convex, if and only if \( a \geq 0 \) and \( ab \geq 4 \).


**b)**
For the minimum value, \(\nabla f = 0\) has to be true

$$
\begin{align}
2a - 6 =^! 0 \\
2b =^! 0
\end{align}
$$

It follows that \( b = 0 \) and \( a = 3 \). Due to the condition \( ab \geq 4 \), the problem is not convex in this case.  

For  
\[
f(1, 1, 0, 3) = 3 \cdot 1^2 + 0 \cdot 1^2 - 4 - 2 + 4 = 3 - 2 = 1 > f(1, 1, 0 , 0) = -4 -2 + 4 = -2,
\]  
this means that \( (1,1) \) is not a local minimum.

{{< /details >}}




## Problem 4

Let \(B\) be symmetric and positiv definit and \(A\) have full rank. Further, \(c\) is not in range of \(A^T\).

Given the problem

$$
\min \ c^Tx \ \ \text{under} \ \ x^TBx \leq 1, \ Ax = 0
$$

a) Show that a minima \(x^*\) exists.  
b) Proof, that \(AB^{-1}A^T\) is regular.  
c) Show that \(\alpha\) exists with \(x^* = \alpha(Pc-B^{-1}c)\), where \(P = B^{-1}A^T(AB^{-1}A^T)^{-1}AB^{-1}\), is \(x^* = 0\)?  
d) Determine \(\alpha\) and \(x^*\).  

{{< details "Solution" "false" >}}

**a)**  
The objective function is continuous. Furthermore, \( M \) is bounded because \( 0 < x^T B x \leq 1 \), and it is closed, thus compact. Since the objective function is continuous and the constraint set is compact, there exists a local solution (LSG).

**b)**  
Since \( A \) has full rank, both \( A \) and \( A^T \) are bijective. Assume \( A B^{-1} A^T x = 0 \).  
Let \( x A B^{-1} A^T x = (A^T x)^T B^{-1} (A^T x) = y^T B^{-1} y \). Then \( y^T B^{-1} y = 0 \) if and only if \( y = 0 \), because \( B^{-1} \) is positive definite.  
It follows that \( x = 0 \). Thus, \( A B^{-1} A^T \) is bijective and, therefore, regular.

**c)**  
The problem is convex because \( f(x) = c^T x \) and \( g(x) = x^T B x - 1 \) are convex, as \( B \) is symmetric and positive definite.  

The Slater condition holds because:  
- The rank of \( A \) is maximal.  
- \( A x' = 0 \) and \( g(x') < 0 \), with \( x' = 0 \).

Thus, there is no duality gap, and a local solution (LSG) exists. We obtain this LSG using the Lagrange multiplier theorem, i.e.,

\[
L(x, u, v) = c^T x + u(x^T B x - 1) + v(Ax)
\]

For the LSG to hold, the following must be true:

\[
\begin{align}
\nabla L = c + 2u B x + A^T v = 0 \\
u g(x) = u(x^T B x - 1) = 0
\end{align}
\]

In particular, \( x^* \neq 0 \), because otherwise, \( u = 0 \) must hold due to the second condition, but then we would have \( c = 0 \) from the first condition, which is impossible according to the assumption, as it would then lie in the image of \( A^T \).

Thus, it follows that \( x^* = - \frac{1}{2} u B^{-1} (c + A^T v) \). Substituting this into \( A x^* = 0 \), we obtain the desired form.

**d)**  
Solving for \( \alpha \) gives the solution.

{{< /details >}}



## Problem 5

Given the function

$$
f(x) = x_1 + 2x_2 + 4x_3 
$$

and the set 

$$
M = \{x_1 x_2 x_3 = 1, \ x_1, x_2, x_3 > 0\}
$$

a) Is M closed? Is M restricted?  
b) Exist a global minima or maxima of f on M?  
c) Determine all local and global minima and maxima of f on M.  

{{< details "Solution" "false" >}}

**a)**  
Let \((a_1), (a_2), (a_3)\) be any sequence in \(M\). Then, it holds that \(a_1 a_2 a_3 \to a^1 a^2 a^3 = 1\), and thus \(M\) is closed.  
\(M\) is not bounded because \((t, 1/t, 0) \to (\infty, 0, 0)\).

**b)**  
There is no maximum point because of the sequence \(a = (t, 1/t, 0) \in M\) and \(f(a) \to \infty\).  
\(M\) is bounded from below because \(x_1, x_2, x_3 > 0\), and we can restrict ourselves to the set \(M = \{ f(x) < f(1, 1, 1) \}\). This set is closed and bounded, hence compact. Since \(f(x)\) is continuous, there exists a minimum point.

**c)**  
The problem is differentiable because \(f(x)\) and \(g(x) = x_1 x_2 x_3 - 1\) are differentiable.  

Let’s examine CQ1:  
- \(\text{Rank}(h) = n\), which is satisfied since we do not have an \(h\) function.  
- \(g(x) + u g'(x) < 0\), which is satisfied for \(x = 0\).

This means we can apply the Lagrange Multiplier Theorem. We first form the Lagrangian function:

\[
L(x, u, v) = x_1 + 2x_2 + 4x_3 + u(x_1 x_2 x_3 - 1)
\]

The LSG (local solution) is a KKT point, for which the following conditions hold:

\[
\begin{align}
0 &= 1 + u x_2 x_3 \\
0 &= 2 + u x_1 x_3 \\
0 &= 4 + u x_1 x_2
\end{align}
\]

Multiply the first equation by \(x_1\), the second by \(x_2\), and the third by \(x_3\), then we obtain \(x_1 x_2 x_3 = 1\).

\[
\begin{align}
x_1 + u &= 0 \\
2 x_2 + u &= 0 \\
4 x_3 + u &= 0
\end{align}
\]

Thus, \(x^* = -u(1, 1/2, 1/4)\). The constraint \(x_1 x_2 x_3 = 1\) gives us \(u = -2\), and therefore \(f(x^*) = 6\).

{{< /details >}}
