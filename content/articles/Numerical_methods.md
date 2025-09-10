---
title: 'Numerical Methods for Computer Scientist'
date: 2025-09-09 09:00:00
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



### Problem 3: QR-Decomposition

Calculate the QR decomposition for

$$A = \begin{pmatrix} 1 & 2 \\ 1 & 2 \\ \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \end{pmatrix}.$$

State all Householder transformations \(Q\) used.


{{< details "Solution" "false" >}}

{{< info "Recap QR-Decomposition" >}}

The prerequisite for the QR decomposition is a matrix \(A\) with full rank. The decomposition is then \(A = QR\), with \(Q\) being an orthogonal matrix and \(R = \begin{pmatrix}\hat{R} \\ 0 \end{pmatrix}\), where \(\hat{R}\) is an upper triangular matrix.

The idea behind it is as follows:
1. Calculate QR-Decomposition, Q orthogonal, R triangularm atrix
2. Solve \(Qc = b\) with \(c = Q^Tb\)
3. Solve \(Rx = c\) through backward subsituino.

We get the decomposition as follows:

1. We consider first the first column \(a_1 \in \mathbb{R}^m\) of our matrix \(A \in \mathbb{R}^{m \times n}\) and choose \(v^{(1)} = a_1 + \text{sgn}(a_{11}) \|a_1\|e_1\). This corresponds to \(\text{sgn}(a_{11})\) as the sign of the first entry of the column vector \(a_1\) and \(\|a_1\| = \sqrt{a_1^T a_1}\) as the Euclidean norm of \(a_1\). Furthermore, we set \(\text{sgn}(0) := 1\). With the vector \(v^{(1)} \in \mathbb{R}^m\), we determine the Householder matrix \(H^{(1)} \in \mathbb{R}^{m \times m}\), which, when multiplied by a matrix \(A\), which we call \(A^{(1)} = H^{(1)}A \in \mathbb{R}^{m \times n}\), yields a matrix whose first column is a multiple of the unit vector.

2. In the next step, we take this matrix \(A^{(1)}\) and strike its first row and column, so that we obtain a smaller submatrix \(A'^{(1)} \in \mathbb{R}^{(m-1) \times (n-1)}\).

3. We now proceed with \(A'^{(1)}\) exactly as we did with \(A\) in Step 1. Explicitly, this means we reflect its first column \(a'_1\) onto a multiple of the first unit vector \(e_1 \in \mathbb{R}^{m-1}\). To do this, we calculate \(v^{(2)} = a'_1 + \text{sgn}(a'_{11}) \|a'_1\|e_1\), and then use this to calculate the \((m-1) \times (m-1)\)-matrix \(H'^{(2)} = E - 2\frac{p^{(2)}(p^{(2)})^T}{\|p^{(2)}\|^2}\). Subsequently, we define our \(m \times m\)-Householder-Matrix \(H^{(2)}\) by
$$
H^{(2)} = \begin{pmatrix} 1 & 0 & \dots & 0 \\ 0 & & & \\ \vdots & & H'^{(2)} & \\ 0 & & & \end{pmatrix}
$$
Now we multiply \(H^{(2)}\) from the left by the previously calculated matrix \(A^{(1)}\). The resulting matrix \(A^{(2)} := H^{(2)}A^{(1)}\) now has zeros below the first two entries in its first column.

4. To achieve the same for the remaining columns, we next strike both the first and second rows and columns of \(A^{(2)}\) and perform Step 3. for the submatrix \(A'^{(2)} \in \mathbb{R}^{(m-2) \times (n-2)}\) and extend it to the \((m-2) \times (m-2)\)-matrix \(H'^{(2)}\) as
$$
H^{(3)} = \begin{pmatrix} 1 & 0 & \dots & 0 \\ 0 & 1 & \dots & 0 \\ \vdots & & H'^{(2)} & \\ 0 & & & \end{pmatrix}
$$
Now we calculate \(A^{(3)} = H^{(3)}A^{(2)}\).

5. This procedure leads us to obtain an upper triangular matrix when we continue until step \(k = \min(m-1, n)\).

{{< /info >}}


We start with the first column vector of the matrix

$$
a_1 =
\begin{pmatrix}
1 \\
1 \\
\sqrt{2}
\end{pmatrix}
$$

Next

$$
||a_1||_2 = \sqrt{1^2 + 1^2 + \sqrt{2}^2} = 2
$$

And calculate the Householder vector

$$
w^1 = a_1 + |a_1|_2 e_1 =
\begin{pmatrix}
1 \\
1 \\
\sqrt{2}
\end{pmatrix} +
2
\begin{pmatrix}
1 \\
0 \\
0
\end{pmatrix} =
\begin{pmatrix}
3 \\
1 \\
\sqrt{2}
\end{pmatrix}
$$

We now calculate the matrix \(Q_1\)

$$
Q_1 = I - 2\frac{w^1 (w^1)^T}{(w^1)^T w^1} =
\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{pmatrix} -
\frac{1}{6}
\begin{pmatrix}
9 & 3 & 3\sqrt{2} \\
3 & 1 & \sqrt{2} \\
3\sqrt{2} & \sqrt{2} & 2
\end{pmatrix} =
\begin{pmatrix}
-1/2 & -1/2 & -\sqrt{2}/2 \\
-1/2 & 5/6 & -\sqrt{2}/6 \\
-\sqrt{2}/2 & -\sqrt{2}/6 & 2/3
\end{pmatrix}
$$

Finally

$$
Q_1 \cdot A =
\begin{pmatrix}
-2 & -3 \\
0 & 1/3 \\
0 & -2\sqrt{2}/3
\end{pmatrix}
$$


Now we can proceed with the second column. Remember, to do this we need to remove the first column and the first row of \(Q_1 A\), which we just calculated.

$$
a_2 =
\begin{pmatrix}
1/3 \\
-2\sqrt{2}/3 \\
\end{pmatrix}
$$

Again we need to calculate the absolute value of it

$$
|a_2| = 1
$$

Thus we get

$$
w^2 = a_2 + |a_2| e_1 = a_2 + e_1 =
\begin{pmatrix}
4/3 \\
-2\sqrt{2}/3 \\
\end{pmatrix}
$$

We can now claulate \(Q_2\)

$$
\hat{Q_2} = = I_2 - 3/4
\begin{pmatrix}
16/9 & -8 \sqrt{2}/9 \\
-8 \sqrt{2}/9 & 8/9
\end{pmatrix} =
\begin{pmatrix}
-1/3 & -2 \sqrt{2}/3 \\
2 \sqrt{2}/3 & 1/9
\end{pmatrix}
$$

Thus our final matrices are

$$
R = Q_2 Q_1 A =
\begin{pmatrix}
1 & 0 & 0 \\
0 & Q_2 \\
0 &
\end{pmatrix}
\begin{pmatrix}
-2 & -3 \\
0 & 1/3 \\
0 & -2\sqrt{2}/3
\end{pmatrix} =
\begin{pmatrix}
-2 & -3 \\
0 & -1 \\
0 & 0
\end{pmatrix}
$$

and

$$
Q = Q_1 \cdot Q_2
$$

{{< /details >}}



### Problem 4: Cholesky- and QR-Decompoaition


Here's the transcript of the image in English:

Let \(A \in \mathbb{R}^{N \times N}\) be an unknown matrix with a decomposition \(A = B^T B\) with a known matrix \(B \in \mathbb{R}^{M \times N}\), \(M \ge N\), given.

a) Determine the property of \(B\) under which \(A\) is symmetric positive definite (spd).

Let \(A\) be spd in the following.

b) State the asymptotic complexity to calculate \(A\) and a Cholesky decomposition of \(A\).

c) Explain how a Cholesky decomposition of \(A\) can be found from a \(QR\)-decomposition of \(B\) without explicitly calculating \(A\).

d) Determine the asymptotic complexity of the procedure in c) including the calculation of the \(QR\)-decomposition and compare it with the complexity from subtask b). State which procedure you would prefer.



{{< details "Solution a)" "false" >}}

Lets first check symmetry:

$$
A^T = (B^TB)^T = B^TB = A
$$

Lets check definitness:

$$
x^TAx = x^TB^TBx = (Bx)^TBx = |Bx|_2^2 \geq 0
$$

But we need \(x^TAx \ge 0\), thus \(B\) needs to have full rank, because then \(Bx \neq 0\).

{{< /details >}}


{{< details "Solution b)" "false" >}}

**Recap Cholesky Decomposition**
The prerequisite for Cholesky decomposition to work is that our matrix $A$ is symmetric and positive definite. The decomposition is then $A = L \cdot L^T$, with $L$ a regular lower triangular matrix.

The idea behind it is as follows:
1. Calculate Choleksy Decomposition \(A = L L^T\)
2. Solve through forward substitution \(Ly = b\)
3. Solve through backward substitution \(L^Tx = y\)

We get the decomposition as follows \(L=(l_{ik})\):

$$
l_{ik} =
\begin{cases}
0, &\text{for } i < k \\
\sqrt{a_{kk} - \sum_{j=1}^{k-1} l_{kj}^2}, &\text{for } i = k \\
\frac{1}{l_{kk}} (a_{ik} - \sum_{j=1}^{k-1} l_{ij}l_{kj}), &\text{for } i > k \\
\end{cases}
$$

The first case in the formula is for the upper corner of the triangular matrix, which contains only 0 entries.

The second case is for the diagonal running from the top-left corner to the bottom-right corner. What we do here is take the entry $a_{kk}$ that lies on the diagonal of matrix $A$, subtract from it the squared sum of all the entries in the same row (from the current matrix $L$), and then take the square root of the result.

The third case is for all the entries in the lower half of the matrix that are not on the diagonal. Here, we take the current entry $a_{ik}$ from matrix $A$, subtract the sum of the products of the corresponding entries that came before it in the same row and column (from matrix $L$), and divide the result by the diagonal entry $l_{kk}$ from the current matrix $L$.

An example is in order:


{{< info "Cholesky Example" >}}

We have the following Matrix given

$$
A =
\begin{pmatrix}
4 & 2 & 6 \\
6 & 2 & 5 \\
6 & 5 & 22 \\
\end{pmatrix}
$$

We want to calculate its Cholesky decomposition. For this, we simply follow the algorithm as laid out previously:


$$
\begin{align}
l_{1,1} &= \sqrt{4} = 2 \\
\\
l_{2,1} &= 2/2 \\
l_{2,2} &= \sqrt{2 - 1^2} = 1 \\
\\
l_{3,1} &= 6/2 = 3 \\
l_{3,2} &= (5 - 3 \cdot 1)/1 = 2 \\
l_{3,3} &= \sqrt{22 - 3^3 - 2^2} = \sqrt{9} = 3
\end{align}
$$

Thus we get

$$
L =
\begin{pmatrix}
2 & 0 & 0 \\
1 & 1 & 0 \\
3 & 2 & 3 \\
\end{pmatrix}
$$

{{< /info >}}

Matrix \(A\) is symmetric, so we only need to calculate half of the matrix entries. Therefore, we have \(\frac{1}{2}(N^2 + N)\) entries to compute. The \(+N\) comes from the fact that we also need to calculate the diagonal.

For each entry, we need to compute a factored sum of \(M\) terms, so in total we have \((N^2 + N) \cdot M\) operations.

For the Cholesky decomposition itself, we need \(\frac{1}{3}N^3\) operations.

Thus, in total, to perform the computation we need:

$$
N^2 \left(M + \frac{1}{3}N \right) + N \cdot M
$$

operations.

{{< /details >}}


{{< details "Solution c)" "false" >}}

So we have \(B = QR\), with \(Q\) being orthogonal, and we want a Cholesky decomposition \(A = LL^T\).

Thus:

$$
A = B^T B = (QR)^T QR = R^T Q^T Q R = R^T R
$$

where \(R = \begin{pmatrix} \hat{R} \\ 0 \end{pmatrix}\), and \(\hat{R}\) is an upper triangular matrix.

Hence, we can set \(L = \hat{R}^T\) to obtain a Cholesky decomposition from a QR decomposition.

{{< /details >}}


{{< details "Solution d)" "false" >}}

The complexity of (b) is \(N^2(M + \frac{1}{3}N)\).

The complexity of QR-Algorithm is \(2N^2(M - \frac{1}{3}N)\)

Now in the case of (c), if \(N < M\) then the complexity is approximately the same. But if \(M >> N\) then QR is much more expensive.

{{< /details >}}



### Problem 5: Cholesky-Decomposition

Let \(\alpha, \beta \in \mathbb{R}\) and

$$A = \begin{pmatrix} \alpha & \beta \\ \beta & 1 \end{pmatrix}$$

Determine for which \(\alpha\) the matrix \(A\) is **positive definite** and derive its **Cholesky decomposition** \(A = LL^T\). Investigate the **stability** of solving the system of equations \(Ax = b\) for a \(b \in \mathbb{R}^2\) using the Cholesky decomposition with respect to the \(\|\cdot\|_1\) norm.


{{< details "Solution" "false" >}}

First we determine positive definitness:

$$
\begin{align}
det_1(A) &= \alpha >^! 0 \\
det(A) &= \alpha - \beta^2 >^! 0 \implies \alpha >^! \beta^2
\end{align}
$$

From this follows for A to be postivi definti \(\alpha > 0\) and \(\alpha > \beta^2).

We are now doing with this a cholesky decompotion, that means \(A = LL^T\) with \(L\) a lower triangular matrix.

$$
A =
LL^T =
\begin{pmatrix}
a & 0 \\
b & c
\end{pmatrix}
\begin{pmatrix}
a & b \\
0 & c
\end{pmatrix} =
\begin{pmatrix}
a^2 & ab \\
ab & b^2 + c^2
\end{pmatrix}
$$

From this follows

$$
a = \sqrt{\alpha}
b = \beta/\sqrt{\alpha}
b^2 + c^2 = 1 \implies c = \sqrt{1 - b^2} = \sqrt{1 - \beta^2/\alpha}
$$

Next we want to ivnestigate the stabiltiy, for this we need the inverse:

$$
A^{-1} = \frac{1}{\alpha-\beta^2}
\begin{pmatrix}
1 & -\beta  \\
-\alpha & \beta
\end{pmatrix}
\quad
L^{-1} = \frac{1}{\sqrt{\alpha - \beta^2}}
\begin{pmatrix}
\sqrt{1 - \beta^2/\alpha} & 0  \\
-\beta/\sqrt{\alpha} & \sqrt{\alpha}
\end{pmatrix}
$$

With this we can calculate the codntion of both matrices to see if using cholesky decomposition introduces additional errors

$$
\begin{align}
K_1(A) &= ||A||_1 ||A^{-1}||_1 \\
&= (\max\{1, \ \alpha\} + |b|)(\frac{1}{(\alpha - \beta)^2}\max\{\alpha, \ 1\} + |b|) \\
&= \frac{1}{(\alpha - \beta)^2} (\max\{\alpha, \ 1\} + |b|)^2
\end{align}
$$

and

$$
\begin{align}
K_1(L)^2 &= (||L||_1 ||L^{-1}||_1)^2 \\
&= ((\max\{\sqrt{\alpha} + \beta/\alpha, \ \sqrt{1 - \beta^2/\alpha}\})(\frac{1}{\sqrt{\alpha - \beta^2}}\max\{\sqrt{\alpha}, \ |\beta|/\sqrt{\alpha} + \sqrt{1-\beta^2/\alpha}\}))^2 \\
&= \frac{1}{\alpha - \beta^2} \max\{\sqrt{\alpha} + |\beta|/\sqrt{\alpha}, \ \sqrt{1 - \beta^2 / \alpha}\}^2 \cdot \max\{\alpha, \ |\beta|/\sqrt{\alpha} + \sqrt{1 - \beta^2/\alpha}\}^2
\end{align}
$$

{{< /details >}}



### Problem 6: Hadamard Approximation

Let \(A \in \mathbb{R}^{N \times N}\) be regular and let \(a_1, \ldots, a_N \in \mathbb{R}^N\) be the columns of \(A\). Show, using the QR-decomposition, Hadamard's inequality:

$$|\det A| \leq \prod_{n=1}^{N} \|a_n\|_2$$

**Hint:** Show that \(\|a_n\|_2 = \|r_{nn}\|_2\), where \(r_{nn}\) are the diagonal elements of \(R\) with index \(n = 1, \ldots, N\).


{{< details "Solution" "false" >}}

We can rewrite \(det(A)\) using the QR-Decomposition

$$
\begin{align}
|det(A)| &= |det(QR)| = |det(Q)det(R)| \\
&= |det(Q)||det(R)| = |det(R)| \\
&= \prod_{n=1}^{N} |r_{nn}|
\end{align}
$$

Further

$$
|a_n|_2 = |Ae_n|_2 = |QRe_n|_2 = |Q||Re_n|_2 = |r_n|_2
$$

and because \(|r_{nn}| \leq |r_n|_2 \), we have our result.

{{< /details >}}



### Problem 7: QR-Decomposition and LGS

Let \(A \in \mathbb{R}^{N \times N}\) be regular and \(\mathbf{b} \in \mathbb{R}^N\). Explain how the linear system of equations \(A\mathbf{x} = \mathbf{b}\) can be solved using the QR-decomposition. Furthermore, state the asymptotic cost of all steps. Examine the procedure for stability with respect to \(\|\cdot\|_2\).


{{< details "Solution" "false" >}}

Solving LGS using QR-Decomposition

$$
Ax = b \iff QRx = b \iff Rx = Q^Tb
$$

Hence

1. Calculate QR- Decomposition, Complexity: \(O(N^3)\).
2. Cauclate \(Q^Tb\), Complexity: \(O(N^2)\)
3. Backward subsituion \(Rx = Q^Tb\). Complexity \(O(N^2)\)

Total Complexity: \(O(N^3)\)

For the stabiltiy/condition: \(K_2(A) = K_2(QR) = K_2(Q)K_2(R)\). Hence the QR -deocmpsotion is table.

{{< /details >}}



### Problem 8: Linear Least Squares Problem

To determine the location of a mobile phone, the directions from which a signal is measured are determined from five transmitting masts. The positions of the transmitting masts in an \((x,y)\)-coordinate system are:

$$
\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Transmitting Mast} & \textbf{M1} & \textbf{M2} & \textbf{M3} & \textbf{M4} & \textbf{M5} \\
\hline
x-Coordinate  & 8  & 22 & 36 & 10 & 13 \\
\hline
y-Coordinate  & 0  & 7  & 18 & 20 & 10 \\
\hline
\tan \alpha   & 1  & -1/2 & 1/2 & -1 & 0  \\
\hline
\end{array}
$$

Here, \(\alpha\) is measured in the mathematically positive sense from the positive \(x\)-axis. Find the position of the mobile phone by formulating a linear least squares problem and then solving it. Explicitly state all defining quantities of the linear least squares problem.

*Hint: Solve the normal equation to solve the least squares problem.*


{{< details "Solution" "false" >}}

Every tranmsiiton mats and its mobile phone togetehr build a line,  where the slope of the line is \(m_i = \tan(\alpha)\). For the slope we also have \(m_i = \frac{y - y_i}{x - x_i}\).
The \(x_i, y_i\) we have given, but the \(x, y\) not, we thus want to rewrite it in such a way that the unknown variables are on one side. Hence

$$
m_i = \frac{y - y_i}{x - x_i} \iff
m_i(x−x_i)=y−yi \iff
m_i x - y = m_i x_i - y_i \iff
m_i x_i  - y_i =: b = m_i x - y
$$

With this we can now clauclate \(b\)

$$
1 \cdot 8 - 0 = 8 \\
-1/2 \cdot 22 - 7 = -18 \\
1/2 \cdot 36 - 18 = 0 \\
-1 \cdot 10 - 20 = -30 \\
0 \cdot 13 - 10 = -10 \\
$$

and our \(A\) matrix weg et from \(m_i x - 1 \cdot y\), thus


$$
A =
\begin{pmatrix}
1 & -1 \\
-1/2 & -1 \\
1/2 & -1 \\
-1 & -1 \\
0 & -1
\end{pmatrix},
\qquad
b =
\begin{pmatrix}
8 \\
-18 \\
0 \\
-30 \\
-10
\end{pmatrix}
$$

The leats quare problem is now

$$
||Ax - b ||_2 = min!
$$

We can now solve this problem using the normal equation \(A^TAx = A^Tb\):

$$
A^TA =
\begin{pmatrix}
5/2 & 0 \\
0 & 5
\end{pmatrix}, \qquad
A^Tb =
\begin{pmatrix}
47 \\
50
\end{pmatrix}
$$

Hence

$$
(x,y)^T = A^TA \dot A^Tb =
\begin{pmatrix}
94/5 \\
10
\end{pmatrix}
$$

{{< /details >}}


### Problem 9: Householder vs. Givens

Given the matrix

$$A = \begin{pmatrix} 3 & 0 & 0 & 4 & 0 \\ 0 & 8 & 0 & 0 & 0 \\ 0 & 0 & 12 & 0 & 5 \\ 4 & 0 & 0 & 24 & 0 \\ 0 & 0 & 5 & 0 & 9 \end{pmatrix}$$

a) Determine a QR-decomposition of \(A\) using Householder transformations.

b) Determine a QR-decomposition of \(A\) using Givens rotations.

c) Explain which of the two methods you would prefer for matrix \(A\) or a general matrix \(B \in \mathbb{R}^{N \times N}\).



{{< details "Solution a)" "false" >}}

We start with

$$
a_1 =
\begin{pmatrix}
3 \\
0 \\
0 \\
4 \\
0
\end{pmatrix}, \quad
|a_1|_2 = \sqrt{25} = 5
$$

and

$$
w_1 = a_1 + |a_1|e_1 =
\begin{pmatrix}
8 \\
0 \\
0 \\
4 \\
0
\end{pmatrix}, \quad
|w_1|_2^2 = 80
$$

With this we can calculate \(Q_1 = I - \frac{2}{|w_1|_2^2} \cdot w_1w_1^T\). Hence

$$
Q_1 =
\begin{pmatrix}
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1 \\
\end{pmatrix} -
\frac{1}{40}
\begin{pmatrix}
64 & 0 & 0 & 32 & 0 \\
0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 \\
32 & 0 & 0 & 16 & 0 \\
0 & 0 & 0 & 0 & 0 \\
\end{pmatrix} =
\frac{1}{40}
\begin{pmatrix}
-24 & 0 & 0 & -32 & 0 \\
0 & 40 & 0 & 0 & 0 \\
0 & 0 & 40 & 0 & 0 \\
-32 & 0 & 0 & 24 & 0 \\
0 & 0 & 0 & 0 & 40 \\
\end{pmatrix}
$$

From this we get

$$
Q_1 \cdot A =
\begin{pmatrix}
-5 & 0 & 0 & -108/5 & 0 \\
0 & 8 & 0 & 0 & 0 \\
0 & 0 & 12 & 0 & 5 \\
0 & 0 & 0 & 56/5 & 0 \\
0 & 0 & 5 & 0 & 9 \\
\end{pmatrix}
$$

The column \(a_2\) is already in the correct form. Thus we can continue with

$$
\hat{a}_3 =
\begin{pmatrix}
12 \\
0 \\
5
\end{pmatrix}, \quad
|\hat{a}_3|_2 = \sqrt{169} = 13
$$

Thus

$$
w_3 =  \hat{a}_3 + |\hat{a}_3|_2 e_1
\begin{pmatrix}
25 \\
0 \\
5
\end{pmatrix}, \quad
|w_3|_2^2 = 650
$$

With this we claulcate \(Q_2 = I - \frac{2}{|w_3|_2^2} \cdot w_3w_3^T\). Hence

$$
Q_2 =
\begin{pmatrix}
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1 \\
\end{pmatrix} -
\frac{1}{325}
\begin{pmatrix}
0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 \\
0 & 0 & 625 & 0 & 125 \\
0 & 0 & 0 & 0 & 0 \\
0 & 0 & 125 & 0 & 25 \\
\end{pmatrix} =
\frac{1}{325}
\begin{pmatrix}
325 & 0 & 0 & 0 & 0 \\
0 & 325 & 0 & 0 & 0 \\
0 & 0 & -300 & 0 & -125 \\
0 & 0 & 0 & 325 & 0 \\
0 & 0 & -125 & 0 & 300 \\
\end{pmatrix}
$$

And with that we finally have

$$
R = Q_2 \cdot Q_1 A =
\begin{pmatrix}
-5 & 0 & 0 & -108/5 & 0 \\
0 & 8 & 0 & 0 & 0 \\
0 & 0 & -13 & 0 & -105/14 \\
0 & 0 & 0 & 56.5 & 0 \\
0 & 0 & 0 & 0 & 83/13 \\
\end{pmatrix}
$$

{{< /details >}}

{{< details "Solution b)" "false" >}}


{{< info "Info ">}}

A Given rotation is defined as

$$
\begin{pmatrix}
c & s \\
-s & c
\end{pmatrix}, \quad c^2 + s^2 = 1
$$

We calculate its value as follows:

If \(|x_n| > |x_m|\) then \(\tau = x_m/x_n = c/s\) and \(s = \sqrt{\frac{1}{ 1+ \tau^2}}\) and \(c = \tau s\)

If \(|x_n| =< |x_m|\) then \(\tau = x_n/x_m = s/c\) and \(c = \sqrt{\frac{1}{ 1+ \tau^2}}\) and \(s = \tau s\)

{{< /info >}}

We calculate

$$
\tau_1 = \frac{4}{3}, \quad c_1 169= \sqrt{\frac{1}{1 + 16/9}} = \sqrt{9/25}=3/5, \quad s_1 = \frac{4}{5}
$$

And with that we get

$$
Q_1 \cdot A =
\begin{pmatrix}
3/5 & 0 & 0 & 4/5 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
-4/5 & 0 & 0 & 3/5 & 0 \\
0 & 0 & 0 & 0 & 1 \\
\end{pmatrix} \cdot A =169
\begin{pmatrix}
-5 & 0 & 0 & -108/5 & 0 \\
0 & 8 & 0 & 0 & 0 \\
0 & 0 & 12 & 0 & 5 \\
0 & 0 & 0 & 56/5 & 0 \\
0 & 0 & 5 & 0 & 9 \\
\end{pmatrix}
$$

We then calculate

$$
\tau_2 = \frac{12}{5}, \quad s_2 = \sqrt{\frac{1}{1 + 144/25}} =5/13, \quad s_1 = \frac{12}{13}
$$

And thus get

$$
R = Q_2 \cdot Q_1A  =
\begin{pmatrix}
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 12/13 & 0 & 5/13 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & -5/13 & 0 & 12/13 \\
\end{pmatrix}
\begin{pmatrix}
-5 & 0 & 0 & -108/5 & 0 \\
0 & 8 & 0 & 0 & 0 \\
0 & 0 & 12 & 0 & 5 \\
0 & 0 & 0 & 56/5 & 0 \\
0 & 0 & 5 & 0 & 9 \\
\end{pmatrix}
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

For \(A\) the Givens method is better as we need less Operation than with Householder.

For \(B\) the Householder method is better as we need less Operation than with Givens method.

It depens on how many entries the matrix has, what is better, the more netries the matrix has the better is Householder.

{{< /details >}}



### Problem 10: Singular Value Decomposition

Let \(A \in \mathbb{R}^{M \times N}\) be a matrix with rank \((A) = R \ne N\) and the singular value decomposition \(A = V \Sigma U^T\) (with singular values \(\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_R > \sigma_{R+1} = \dots = \sigma_N = 0\) and \(b \in \mathbb{R}^M\). We define

$$\Sigma_k = \text{diag}(\sigma_1, \dots, \sigma_k) \in \mathbb{R}^{k \times k},$$
$$A_k = V \begin{pmatrix} \Sigma_k & 0 \\ 0 & 0 \end{pmatrix} U^T = \sum_{r=1}^k \sigma_r v^r (u^r)^T.$$

Since \(A\) does not have full rank, the linear least squares problem (LAP)

$$|Ax - b|_2 = \min!$$

has infinitely many solutions (compare script). We further define

$$x^k = A_k^\dagger b, \quad x^* = x^R, \quad A_k^\dagger = U \begin{pmatrix} \Sigma_k^{-1} & 0 \\ 0 & 0 \end{pmatrix} V^T \in \mathbb{R}^{N \times M},$$
$$r^k = b - Ax^k, \quad \Sigma_k^{-1} = \text{diag}(1/\sigma_1, \dots, 1/\sigma_k) \in \mathbb{R}^{k \times k}.$$

In the task, it is to be shown that the solution to (LAP) given by \(x^*\) and \(x^k\) approximates the solution by minimal Euclidean norm. It is known from the lecture that \(x^*\) is a solution to (LAP). Now show that

a) It holds that \(x^k = \sum_{r=1}^k \frac{1}{\sigma_r} (b^T v^r) u^r\).

b) Determine \(|x^k|_2^2\).

c) For arbitrary \(k \le l \le R\) it holds that \(|r^k|_2^2 \ge |r^l|_2^2\) and \(|x^k|_2^2 \le |x^l|_2^2\).

d) For all other solutions \(x\) of (LAP) it holds that \(|x|_2 \ge |x^*|_2\).

Hint: Represent \(x\) in the form \(x = \sum_{n=1}^N u^n \alpha_n\), where \(u^{R+1}\) to \(u^N\) form an orthonormal basis for the kernel of \(A\).


{{< details "Solution a)" "false" >}}

$$
\begin{align}
x^k = A_k^\dagger b
&=U \sigma_k V^T b \\
&=U \sigma \sum_{m=1}^{R} (v^{m})^T b \\
&=U \text{diag}(1/\sigma_1, \dots, 1/\sigma_k) \sum_{r=1}^{R} (v^{r})^T b \\
&=U \sum_{r=1}^{R} (1/\sigma_r) (v^{r})^T b \\
&=\sum_{r=1}^{R} (1/\sigma_r) (v^{r})^T b u^m \\
\end{align}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

$$
\begin{align}
|r^k|_2^2 &= |b - Ax^k|_2^2 = |b - A A_k^\dagger b| \\
&= |b - V\sigma_kU^TU\sigma_k^{-1}V^Tb|  \\
&=|b - V\sigma_k\sigma_k^{-1}V^Tb| \\
&=|b - V\begin{pmatrix} I & 0 \\ 0 & 0 \end{pmatrix}V^Tb| \\
&=|(I - V\begin{pmatrix} I & 0 \\ 0 & 0 \end{pmatrix})V^T)b| \\
&=|(VIV^T - V\begin{pmatrix} I & 0 \\ 0 & 0 \end{pmatrix})V^T)b| \\
&=|V(I - \begin{pmatrix} I & 0 \\ 0 & 0 \end{pmatrix}))V^Tb|\\
 &=^{V doesnt change length} |V(\begin{pmatrix} 0 & 0 \\ 0 & I \end{pmatrix}))V^Tb| \\
&= |\begin{pmatrix} 0 & 0 \\ 0 & I \end{pmatrix})V^Tb| \\
&=|V^Tb : {u+ 1 : R}|
\end{align}
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

For \(k = l\) the statement is trivially true.

Let \(k < l\)

$$
|r^k|_2^2 - |r^l|_2^2 =^{(b)} |V^Tb : {u+ 1 : R}|_2^2 > 0 \implies |r^k|_2^2 > |r^l|_2^2
$$

$$
|x^k|_2^2 - |x^l|_2^2 =^{(a)} - |\sum 1/\sigma (v^r)^Tbu^r| < 0 \implies |x^k|_2^2 < |x^l|_2^2
$$

{{< /details >}}


{{< details "Solution d)" "false" >}}

Nope

{{< /details >}}



### Problem 11: QR-Algorithm and Inverse Iteration

Given the matrix

$$
A =
\begin{pmatrix}
8 & \frac{12}{5} & -\frac{9}{5} \\
\frac{12}{5} & \frac{109}{25} & \frac{12}{25} \\
-\frac{9}{5} & \frac{12}{25} & \frac{116}{25}
\end{pmatrix}
$$

In this Problem the task is to caluclate the Eigenvalues of \(A\).

a) Transform \(A\) into a Hessian-Matrix.

b) Do the first step of the \(QR\)-Iteration with Shift.

c) Do the next Step of the inverse Iteration with Shift with the starting value \(v^0 = e^3\) and \(v^0 = e^2\).


{{< details "Solution a)" "false" >}}

First thing to notice is that \(A\) is symmetrical, thus all Eigenvalues are real and \(H\) is tridiagonal.

To transform our matrix we can use N-2 householder transformations.

Hence we start with the first column

$$
v_1 =
\begin{pmatrix}
\frac{12}{5} \\
-\frac{9}{5}
\end{pmatrix}, \quad
|v_1|_2 = \sqrt{144/25 + 81/25} = 15/5 = 3
$$

and

$$
a_1 = v_1 + |v_1|e_1 =
\begin{pmatrix}
\frac{27}{5} \\
-\frac{9}{5}
\end{pmatrix}, \quad
|a_1|_2^2 = 810/25
$$

With this we can calculate \(Q = I - \frac{2}{|a_1|_2^2 a_1a_1^T}\). Hence

$$
Q =
\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{pmatrix} -
\frac{2}{810}
\begin{pmatrix}
0 & 0 & 0 \\
0 & 729 & -243 \\
0 & -243 & 81
\end{pmatrix} =
\frac{1}{405}
\begin{pmatrix}
405 & 0 & 0 \\
0 & -324 & 243 \\
0 & 242 & 324
\end{pmatrix}
$$

We can now calculate the Hessian matrix as follows

$$
H = QAQ =
\begin{pmatrix}
8 & -3 & 0 \\
-3 &  4 & 0 \\
0 & 0 & 5
\end{pmatrix}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

{{< info "Info" >}}

The *simple QR-Algorithm* to find out the Eigenvalue works as follows:

1. Set \(A_0 = A\) and \(k = 0\)
2. Decompose \(A_k = Q_kR_k\) (QR-Decompostiton)
3. Calculate \(A_{k+1} = R_kQ_k\)

To increase convergence speed, we can use shifts:

1. Set \(H-0 = H\) and \(k=0\)
2. Decompose \(H_k - \mu_k I_N = Q_kR_k\)
3. Calculate \(H_{k+1} = R_kQ_k + \mu I_n\) increase \(k\) by \(1\) and go to step 2.

With \(\mu = h^k_{n,n-1}\) if \(\leq \epsilon\) else \(\mu = h^k_{n-1,n-1}\). If \(n=1\) the algorithm stops.

{{< /info >}}


Because we have not many entries in our matrix we can use the Givens transformation, see Problem 9c), for the QR-Decomposition.

In task (a) we already did Step 1.

Because \(h_{3,2} = 0\) we use \(\mu = h_{2,2} = 4\). We Now compute \(H_k - \mu I_n\)

$$
H_0 - 4 I_3 =
\begin{pmatrix}
4 & -3 & 0 \\
-3 &  0 & 0 \\
0 & 0 & 1
\end{pmatrix}
$$

We now use Givens rotation to calculate QR-Decomposition. Because \(c = 4 > -3 = s\) we get \(\tau=s/c\), hence

$$
\tau = -3/4, \quad c = \sqrt{\frac{1}{1+ \tau^2}} = \frac{4}{5}, \quad s = \tau \cdot c = -\frac{3}{5}
$$

With this we get

$$
Q =
\begin{pmatrix}
c & s & 0 \\
-s & c & 0 \\
0 & 0 & 1
\end{pmatrix} =
\begin{pmatrix}
4/5 & -3/5 & 0 \\
3/5 & 4/5 & 0 \\
0 & 0 & 1
\end{pmatrix}
$$

We now need to compute \(R\)

$$
R = Q \cdot (H_0 - 4 I_3) =
\begin{pmatrix}
5 & -12/5 & 0 \\
0 & -9/5 & 0 \\
0 & 0 & 1
\end{pmatrix}
$$

And can now do Step 3 \(H_{k+1} = R_kQ_k + \mu I_n\)

$$
H_2 =
\begin{pmatrix}
136/25 & 27/25 & 0 \\
27/25 & -36/25 & 0 \\
0 & 0 & 1
\end{pmatrix} + \mu I_3 =
\begin{pmatrix}
236/25 & 27/25 & 0 \\
27/25 & 64/25 & 0 \\
0 & 0 & 1
\end{pmatrix}
$$

With this we are finished, as we reached \(n=1\), see stop criteria.

Our eigenvalues are \(64/25=2.56\) and (27=25=1.08).

{{< /details >}}


{{< details "Solution c)" "false" >}}

{{< info "Info" >}}

Algorithm *Inverse Iteration with Shift* for Eigenvalue calculation

1. Choose \(v^0 \in \mathbb{R}^n\) with \(|v^0| = 1\), set \(k=0\), choose \(\epsilon > 0\)
2. \(\mu_k = r(A, v^k) = \frac{(v^k)^TAv^k}{v^k)^TV^k}\) and if \(|Av^k - \mu v^k| < \epsilon\) then Stop
3. \(w^k = (A - \mu_k I_v)^{-1}v^k\) and \(v^{k+1} = w^k/|w^k|\)
4. \(k \to k+1\) and go to Step 2

{{< /info >}}


Our start vector is \(v^0 = e^3 = (0,0,1)^T\). Hence in Step 1

$$
\mu_1 = r(H, v^0) = \frac{(e^3)^THe^3}{(e^3)^Te^3} = \frac{5}{1} = 5
$$

Further

$$
|He^0 - \mu_1 e^3| = |He^0 - 5 e^3|  = 0
$$

Thus we are finished, because we reached the STOP criteria.

We now use the second startvector \(v^0 = e^2 = (0,1,0)^T \). Hence in Step 1

$$
\mu_1 = r(H, v^0) = \frac{(e^2)^THe^2}{(e^2)^Te^2} = \frac{4}{1} = 4
$$

Further

$$
|He^0 - \mu_1 e^2| = |He^0 - 4 e^2|  = 3 > 0
$$

We have not reached the Stop criteria. We continue with Step 3

$$
w^0 = (A - 4 I_3)^{-1}v^0 =
\begin{pmatrix}
0 & -1/3 & 0 \\
-1/3 & -4/9 & 0 \\
0 & 0 & 1
\end{pmatrix} v^0 =
\begin{pmatrix}
-1/3 \\
-4/9 \\
0
\end{pmatrix}
$$

And

$$
|w^0|_2 = \sqrt{1/9 + 16/81} = 8/9
$$

Hence

$$
v^{1} = w^0 / |w^0| =
\begin{pmatrix}
-3/5 \\
-4/5 \\
0
\end{pmatrix}
$$

We now do Step 2 again with our new vector

$$
\mu_2 = r(H, v^1) = 2.56
$$

And

$$
|He^2 - \mu_1 v^1| \approx 1.08 > 0
$$

Our eigenvalues are \(2.56\) and (1.08).

{{< /details >}}


### Problem 12: QR-Algorithm and Similarity

Let \(A \in \mathbb{R}^n\) symmetrical. Show that all \(A_k\) in \(QR\)-Algorithm with an arbitrarily shift are similar to \(A\), that is they have the same eigenvalues.


{{< details "Solution" "false" >}}

We have

$$
A_k = Q_kR_k \mu I_n \iff Q_k R_k = A_k - \mu I_n \iff R_k = Q^T(A_k - \mu I_n)
$$

Hence

$$
\begin{align}
A_{k+1} &= R_kQ_k \mu I_n \\
    &= Q^T(A_k - \mu I_n)Q_k + \mu I_n  \\
    &= Q^TA_kQ_k - \mu Q^TQ_k + \mu I_n \\
    &= Q^TA_kQ_k - \mu + \mu I_n \\
    &= Q^TA_kQ_k\\
\end{align}
$$

Thsu we have shown for \(n=k+1\) that \(A_n\) is similar to \(A_k\). We continue inductively

$$
Q^TA_kQ_k =  Q_k^T Q_{k-1}^T \cdot \dots \cdot Q_0^T A_0 Q_0 \cdot \dots \cdot Q_{k-1} Q_{k}
$$

With \(A := A_0\), \(\hat{Q}^{-1} := Q_k^T Q_{k-1}^T \cdot \dots \cdot Q_0^T\) and  \(\hat{Q_0} := Q_0 \cdot \dots \cdot Q_{k-1} Q_{k}\).

And \(A_{k+1} = \hat{Q}^{-1} A \hat{Q}\), we thus have a similarity.

{{< /details >}}


### Problem 13: Linear Iteration

a) Let \(|\cdot|\) be a vectornorm and \(||\cdot||\) be the induced matrix norm. Further let the pre-condition be \(B \approx A^{-1} \in \mathbb{R}^{n \times n}\) and the matrix norm so that \(||I_n - BA|| \le 1\). The solution for the linear equatio nsystem \(Ax = b\) with \(b \in \mathbb{R}^N\) is called \(x \in \mathbb{R}^N\).
Show that the error of the \(k\)-th iteratiation \(|x^k - x|\)  can be approxmiates using the error of the first iteration \(|x^0 - x|\) and with that, that \(x^k \to x\)

b) Given the system ofl ienar equation \(Ax = b\) and a general lienar iterations method with the vector condition \(B\). Further we have a speectral radius of \(p(I_N - BA) \ge 1\).
Show that , a general linear iteration method for bad starting value \(x^0\) diverges.


{{< details "Solution a)" "false" >}}

{{< info "Info" >}}

The **general linear iteration** can be used to solve systems of linear euqations.

1. Choose a starting Value \(x^0\) and a tolerance \(\epsilon\) with \(r^0 := b -Ax^0\)
2. If \(|r^k| \leq \epsilon\) Stop
3. Calculate
$$
\begin{align}
c^k &= Br^k \\
x^{k+1} &= x^k + c^k \\
r^{k+1} &= r^k - Ac^k \\
\end{align}
$$

With \(r^k - Ac^k = b - Ax^k - Ac^k = b - A(x^k +c^k) = b - Ax^{k+1}\)

{{< /info >}}

We know that \(x = A^{-1}b\). Further

$$
\begin{align}
|x^{k+1} - x| &= |x^k + c^k - x| \\
              &= |x^k + B(b - Ax^k) - x| \\
              &= |x^k + Bb - BAx^k - x| \\
              &= |(I_n - BA)x^k + Bb - x| \\
              &= |(I_N - BA)(x^k - A^{-1}b)| \\
              &\leq ||I_n -BA|| |x^k  -x|
\end{align}
$$

If we now set \(q := ||I_n - BA||\) then we have \(|x^{k+1} - x | \leq q^{k+1} |x^0 - x|\)

And because of the problem at hand \(q < 1\), see problem text. This means \(q^k \to 0\).

{{< /details >}}


{{< details "Solution b)" "false" >}}

We define \(v := e^0 = x - x^0\) as eigenvector of \(C := I_n - BA\) with the eigenvalue \(\lambda\) with \(|\lambda| > 1\).

From this follows

$$
\begin{align}
|e^{k+1}| &=^{a)} |(I_n - BA)^{k+1}e^0| \\
          &= |(I_n - BA)^k Cv| \\
          &= |(I_n - BA)^k \lambda v| \\
          &=^{\text{induction}} | \lambda^{k+1} v| \\
          &= |\lambda|^{k+1} |v| \to \infty\\
\end{align}
$$

{{< /details >}}



### Problem 14: Linear Iteration

Given the following system of lienar equations \(Ax = b\)

$$
A =
\begin{pmatrix}
2 & 1 & 4 \\
1 & 2 & -4 \\
4 & 4 & 2
\end{pmatrix}
$$

Show that for an arbitariy start value \(x^0\) and right side \(b\) with the norm \(|\cdot|_2\):

a) That the Jacobi-Method converges for \(A\)

b) That the Gauß-Seidel-Method diverges for \(A\)



{{< details "Solution a)" "false" >}}

{{< info "Info" >}}

To do lienar iteration with the **jacobi method**

1. decompose our matrix \(A\) into
$$
A = L + D + R
$$
2. Calculate the inverse \(B = D^{-1}\) of the diagonal matrix.
3. The Iteration matrix is then \(C = I - BA\)
4. We Repeat step 3.
5. We calculate the Eigenvalue using \(det(\lambda I - C)\)

Importantly our method converges if \(C = ||I_N - BA|| < 1\).

{{< /info >}}

We first cauclate thei nvers of the diaognal matrix

$$
B = D^{-1} =
\begin{pmatrix}
1/2 & 0 & 0 \\
0 & 1/2 & 0 \\
0 & 0 & 1/2
\end{pmatrix}
$$

We can use this to do the first step

$$
c_1 = I_3 - BA = I_3 - \frac{1}{2}A =
\begin{pmatrix}
0 & -1/2 & -2 \\
-1/2 & 0 & 2 \\
-2 & -2 & 0
\end{pmatrix}
$$

We determien the eigenvvalues

$$
det(\lambda I_3 - C_1) det(
\begin{pmatrix}
\lambda & 1/2 & 2 \\
1/2 & \lambda & -2 \\
2 & 2 & \lambda
\end{pmatrix}
) =
\lambda^3 - 2 + 2 - \lambda(1/4 + 4 - 4) =
\lambda(\lambda^2 - 1/4) =
\lambda(\lambda - 1/2)(\lambda + 1/2)
$$

Thus the eigenvalues are \(\lambda_1 = 0, \lambda_2 = -1/2, \lambda_3 = 1/2\).

Further \(p(c_1) = ||C_1|| = 1_2 < 1\), thus jacobi sentence converges.

{{< /details >}}


{{< details "Solution b)" "false" >}}


{{< info "Info" >}}

To do lienar iteration with the **Gauß-Seidel method**

1. decompose our matrix \(A\) into
$$
A = L + D + R
$$
2. Calculate the inverse \(B = (L + D)^{-1}\).
3. The Iteration matrix is then \(C = I - BA\)
4. We Repeat step 3.
5. We calculate the Eigenvalue using \(det(\lambda I - C)\)

Importantly our method converges if \(C = ||I_N - BA|| < 1\).

{{< /info >}}

We calculate first

$$
B = (L + D)^{-1} =
\begin{pmatrix}
2 & 0 & 0 \\
1 & 2 & 0 \\
4 & 4 & 2
\end{pmatrix}^{-1} =
\begin{pmatrix}
1/2 & 0 & 0 \\
-1/4 & 1/2 & 0 \\
-1/2 & -1 & 1/2
\end{pmatrix}^{-1}
$$

Hence

$$
C_2 = I_3 - BA =
\begin{pmatrix}
0 & -1/2 & -2 \\
0 & 1/4 & 3 \\
0 & 1/2 & -2
\end{pmatrix}
$$

We claculate the eigenvalues

$$
det(\lambda I_3 - C_2) =
det(\begin{pmatrix}
\lambda & 1/2 & 2 \\
0 & \lambda-1/4 & -3 \\
0 & -1/2 & \lambda+2
\end{pmatrix}) =
\lambda
det(
\begin{pmatrix}
\lambda - 1/4 & -3 \\
-1/2 & \lamda + 2
\end{pmatrix} =
\lambda((\lambda - 1/2)(\lambda + 2) - 3/2) =
\lambda(\lambda^2 + 7/4\lambda -2)
)
$$

We know that 2 eigenvalues exist with

$$
(\lambda - \lambda_1)(\lambda - \lambda_2) = lambda^2 + 7/4\lambda -2
$$

And

$$
... + \lambda_1\lambda_2 = ... -2
$$

Hence \(|\lambda_1| > 1\) or \(|\lambda_2| > 1\).

Thus \(p(C_2) = |C_2| > 1\). It can diverge

{{< /details >}}


### Problem 15: CG-Method

Given the linear system of equations:

$$
\begin{pmatrix}
1 & 0 & 1 \\
0 & 2 & 0 \\
1 & 0 & 3
\end{pmatrix}
\mathbf{x} =
\begin{pmatrix}
4 \\
4 \\
4
\end{pmatrix}
$$

a) Determine the exact solution $\mathbf{x}^* \in \mathbb{R}^3$ of the linear system of equations.

b) Calculate 3 steps of the **CG-method** for the linear system of equations. Choose the starting vector $\mathbf{x}^0 = (0, 0, 0)^T$ and use the identity as a preconditioner.


{{< details "Solution a)" "false" >}}

We can see from the matrix that \(2x_2 = 4 \iff x_2 = 2\).

We can subtract teh first equation from the second and get

$$
2x_3 = 0 \iff x_3 = 0
$$

Inserting this in the first equation we gwet \(x_1 = 4\).


{{< /details >}}


{{< details "Solution b)" "false" >}}

{{< info "Info" >}}

To use the **CG-Method** we use the energy norm

$$
||x||_A = \sqrt{x^Tx}
$$

its scalaproduct is

$$
<x,y>_A = x^TAy
$$

The matrix A needs to be **symmetrical** and **positiv definit**. We can then proceed as following

1. choose \(x_0 \in \mathbb{R}^n\). Calculate
$$
r^0 = b -Ax^0
$$
$$
w^0 = Br^0
$$
$$
p_0 = (w^0)r^0
$$
and set \(d^1 := w^0, \ k := 0\).

2. If \(p_k \leq \epsilon\) then stop else continue
3. Set \(k := k +1\) and calculate
$$
\begin{align*}
u^k &= Ad^k \\
\alpha_k &= p_k -1 /(u^k)^T d^k \\
x^k &= x^{k+1} + \alpha_k d^k \\
r^k &= r^{k-1} - \alpha_k d^k \\
w^k &= Br^k \\
p_k &= (w^k)^Tr^k \\
d^{k+1} = w^k + p_k/p_k-1 d_k
\end{align*}
$$
5. Go to Step 2

Whereby \(B\) is an invertierable matrix called the **precondition** to solve \(Ax =b\) with \(BAx = Bb\), where B should be choosen so that \(BA\) condisiton is small.

{{< /info >}}

Because \(B = I_3\) we get \(w^k = r^k\), further

1. $$
\begin{align*}
r^0 &= b -Ax^0 = b  \\
p_0 &= (w^0)r^0 = |r_0|^2_2 = 48 > 0 \\
d^k = r^0
\end{align*}
$$

2. $$
\begin{align*}
u^1 &= (8 \ 8 \ 16)^T \\
\alpha_1 &= 3/8 \\
x^1 = (1 \ 1 \ -2) \\
p_1 = 6 \\
d_2 = (4/2 \ 3/2 \ -3/2)^T  \\
\end{align*}
$$

This continues for two steps. After which it stops because of \(p_0 = 0\).

{{< /details >}}



### Problem 16: Newton-Method

Given the non-linear system of equations:

$$
\mathbf{F}(\mathbf{x}) = \begin{pmatrix}
\exp(x_1^2) - \exp(x_2^2) + x_1x_2 - e \\
x_1x_2
\end{pmatrix} = \begin{pmatrix}
0 \\
0
\end{pmatrix}
$$

a) Determine all exact solutions of this system of equations.

b) Perform the first iteration step of the **Newton's method** for the starting values, if possible:

$$\mathbf{x}^0 = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \quad \text{and} \quad \mathbf{x}^0 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$$

c) Justify why the fixed-point iteration

$$\mathbf{x}^{k+1} = \mathbf{x}^k - B \cdot \mathbf{F}(\mathbf{x})$$

with the matrix

$$
B = \begin{pmatrix}
\frac{1}{2\pi} & 0 \\
0 & 1
\end{pmatrix}
$$

**locally converges linearly**.


{{< details "Solution a)" "false" >}}

From \(x_1x_2 = 0\) follows \(x_1 = 0\) or \(x_2 = 0\).

**Case 1: \(x_1 = 0\)**

$$
-exp(x_2^2) + 1 - e = 0 \iff -exp(x_2^2) = e - 1
$$

Has no solution since \(-exp(x_2^2) < 0 \) and \(e - 1 > 0\).


**Case 2: \(x_2 = 0\)**

$$
exp(x_1^2) = e + 1 \iff \pm \sqrt{ln(e + 1)}
$$

Hence

$$
x \in \{(\sqrt{ln(e + 1)}, 0), \ (-\sqrt{ln(e + 1)}, 0)\}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

{{< info "Info" >}}

The **newton-method** can be used to solve non-linear systems of equations..

1. Choose a starting value \(x^0\) and a tolerance \(\epsilon\)
2. Solve \(f'(x^k)d^k = -f(x^k)\) you can use LR-Decomposition for this, then calculate \(x^{k+1} = x^k + d^k\)
3. If \(||d_k|| \le \epsilon\) then Stop, else increase \(k\) by \(1\) and go to Step 1.

This can be simplified to the following formula

$$
x^{k+1} = x^k - Bf(x^k)
$$

this is called **simplified newton method**.

The method is locally linear convergent if

$$
p(C) = p(I - BF'(x^*)) < 1
$$

{{< /info >}}

We first calculate the derivatice

$$
DF(x) =
\begin{pmatrix}
2x_1 exp(x_1^2) + x_2 & x_1 - 2x_2 exp(x_1)^2 \\
x_2 & x_1
\end{pmatrix}
$$

For \(x^0 = (0 \ 0 )^T\) is

$$
DF(x) =
\begin{pmatrix}
0 & 0 \\
0 & 0
\end{pmatrix}
$$

Hence the newton method is not defined.


For \(x^0 = (1 \ 1 )^T\) is

$$
DF(x^0) =
\begin{pmatrix}
2e + 1 & 1-2e \\
1 & 1
\end{pmatrix}
$$

and

$$
-F(x^0) =
\begin{pmatrix}
e-1 \\
-1
\end{pmatrix}
$$

Thus

$$
\begin{align*}
&(I) \quad (2e+1)x_1 (1-2e)x_2 = e - 1 \\
&(II) \quad x_1 + x_2 = - 1
\end{align*}
$$

We solve this by \((I) - (II)\):

$$
(I') \quad x_1 - x_2 = 1/2
$$

and \(I' + (II)\) results in \(x_1 = -1/4, \ x_2 = -3/4\).

Hence

$$
x^1 = x^0 + d^0 = (1 \ 1)^T + (-1/4 \ -3/4)^T = (3/4 \ 1/4)^T
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

We need to show \(p(C)=p(I - BDF(x^*)) < 1\).

From (a) we know that the solution is \(x^* = \sqrt{ln(e+1)} \ 0\)^T.

Hence

$$
C = I_2 - B \cdot DF(x^*)  = I_2 -
\begin{pmatrix}
\sqrt{ln(e + 2)}(e+1) & \sqrt{ln(e +1)/2 \pi} \\
0 & \sqrt{ln(e+1)}
\end{pmatrix} =
\begin{pmatrix}
(\pie - \sqrt{ln(e+2)}(e+1))/\pie & * \\
0 & 1 - \sqrt{ln(e+1)}
\end{pmatrix} \
$$

Thus

$$
p(C) \approx |(\pie - 1.15 - 3.7)/\pie| < 1
$$

{{< /details >}}


### Problem 17: Polynomial interpolation

a) Given the support points $\xi_0 < \dots < \xi_N$ and the values $f_0, \dots, f_N$. The corresponding **Lagrange interpolation problem** (cf. script) is:

Determine a polynomial $P \in \mathbb{P}_N$ with

$$P(\xi_n) = f_n, \quad n=0, \dots, N.$$

Show that the solution to this interpolation problem is **unique**.


{{< details "Solution a)" "false" >}}

Assume: it exist \(P,Q \in \mathbb{P}_N\) which solves \(P(\xi) = f_n\) with \(P \neq Q\).

Then \(P-Q \in \mathbb{P}_N\) and \(P(\xi) - Q(\xi) = 0\).

\(P - Q\) hat maximal N-roots in the complex numbers.

But \(\xi_n\) for \(n=0,...,N\) are roots of \(P-Q\), these are N+1 roots, contraddiction.

Hence \(P = Q\), there is only on poylnomial.

{{< /details >}}

## Problem 18: Schema of Neville

Given the table of values:

$$
\begin{array}{|c|c|c|c|c|c|}
\hline
n & 0 & 1 & 2 & 3 \\
\hline
\xi_n & -1 & 0 & 1 & 3 \\
\hline
f_n & 8 & 3 & 4 & 8 \\
\hline
\end{array}
$$

a) Determine the **interpolation polynomial** \(p \in \mathbb{P}_3\) with \(p(\xi_n) = f_n\) for \(n=0, 1, 2, 3\) in **Newton form**.

b) Extend the interpolation polynomial by including \((\xi_4, f_4) = (2, 1)\).


{{< details "Solution a)" "false" >}}

{{< info "Info" >}}

To calculate the **newton poylnomial**

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 50%" src="/attachments/numerical_methods/recursive_newton.png">
</figure>
{{< /rawhtml >}}

The main diagonal are the coefficients of the newton polynomial.


{{< /info >}}


{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 100%" src="/attachments/numerical_methods/numerical_method_polynomialinterpolation.png">
</figure>
{{< /rawhtml >}}

{{< /details >}}


{{< details "Solution b)" "false" >}}

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 100%" src="/attachments/numerical_methods/polynomial_interpolation_2.png">
</figure>
{{< /rawhtml >}}

{{< /details >}}


## Problem 19: Fast Cubic Spline

Given the nodes \(\xi_0 = -1, \xi_1 = 0\) and \(\xi_2 = 1\) on the interval \([-1, 1]\). Consider the function

$$
f(t) = \begin{cases}
(t+1) + (t+1)^3 & \text{for } -1 \le t \le 0 \\
4 + (t-1) + (t-1)^3 & \text{for } 0 < t \le 1.
\end{cases}
$$

a) Justify which properties of a **cubic spline with natural boundary conditions** the function \(f\) fulfills and which it does not.

b) Change the function \(f\) on the subinterval \((0, 1]\) so that \(f\) fulfills all properties of a cubic spline with natural boundary conditions.
*Hint: The function \(f\) does not need to fulfill any interpolating properties.*


{{< details "Solution a)" "false" >}}

First calculate the derivatives

$$
\begin{align*}
f_1'(t) &= 1 +3(t+1)^2  \\
f_1''(t) &= 6(t+1) \\
f_2'(t) &= 1+ 3(t-1)^2 \\
f_2''(t) &= 6(t-1) \\
\end{align*}
$$

Properties

$$
(i) f_1, f_2 \in \mathbb{P}_3
$$

$$
(ii) Smoothness:
f_1(0) = 2 = f_2(0)
f_1'(0) = 4 = f_2'(0)
f_1'(0) = 6 \neq -6 = f_2''(0)
$$

$$
(iii) Natural:
f_1''(-1) = 0
f_2''(1) = 0
$$

Thus \(f\) fulfills all properties besides continuity in the second derivative in \(t=0\).

{{< /details >}}


{{< details "Solution b)" "false" >}}

For (a) following applies:

$$
\begin{align*}
(I) f_2(0) &= 2 \\
(I) f_2'(0) &= 4 \\
(I) f_2''(0) &= 6 \quad f_2''(1) = 0
\end{align*}
$$

From (III) follows \(f_2''(t) = 6\).

$$
f_2'(t) = -(1-t)^2 + c
$$

with (II) follows: \(f_2'(0) = -3(1 - 0)^2\).

with (II) follows: \(f_2'(0)\ = -3(1-0)^2 + c =^! u\)

follows \(c=7\), hence \(f_2'(0)\ = -3(1-0)^2 + 7\).

In total we have \(f_2(t) = (1-t)^3 +7t + 1\).

{{< /details >}}


## Problem 20: Determining of Weights

Determine the weights \(\omega_0, \omega_1, \omega_2\) for \(\xi_0 = -\frac{h}{2}, \xi_1 = 0\) and \(\xi_2 = \frac{h}{2}\), such that

$$
\int_{-h}^h P(t) \,dt = \sum_{n=0}^2 \omega_n P(\xi_n)
$$

is exact for polynomials \(P \in \mathbb{P}_2\).



{{< details "Solution" "false" >}}

The basis of \(\mathbb{P}_2\) is \(\{1, x, x^2\}\). Hence the condition of the task is fullfileld when its fullfileld for the basis.

We get the following conditions

$$
\begin{align}
\int 1 dt &= [t]^{h}_{-h} = 2h =^{?} \sum w_n 1(\xi_n) = w_0 + w_1 + w_2 \\
\int t dt &= [\frac{1}{2}t^2]^{h}_{-h} = 0 =^{?} \sum w_n t(\xi_n) = -\frac{h}{2} w_0 + \frac{h}{2}w_2\\
\int t^2 dt &= [t]^{h}_{-h} = \frac{2}{3}h^3 =^{?} \sum w_n t^2(\xi_n) = \frac{h^2}{4}w_0 + \frac{h^2}{4}w_2\\
\end{align}
$$

From (2) follows \(w_0 = w_2\). In (3) we thus get \(\frac{h^2}{2}w_0 = \frac{2}{3}h^3\), from this follows \(w_0 = \frac{4}{3}h = w_2\). In (1) we have \(\frac{8}{3}h + w_2 = 2h\) from this follows \(w_1 = -\frac{2}{3}h\).

{{< /details >}}


## Problem 21: Composite (left-sided) rectangle rule

Given is \(f \in C^1[a,b]\), as well as the equidistant nodes for \(n = 0, \dots, N\)
$$\xi_n = a + nh \quad \text{and} \quad h = (b-a)/N.$$

The composite (left-sided) rectangle rule is defined by

$$
Q(f) = \sum_{n=1}^N h f(\xi_{n-1}).
$$

Show the error estimate

$$ \left| \int_a^b f(t) \,dt - Q(f) \right| \leq \frac{b-a}{2} h \sup_{t \in [a,b]} |f'(t)|.$$


{{< details "Solution" "false" >}}

From \([\xi_{n-1}, \xi_{n}]\) follows fro mthe taylor series development

$$
f(t) = f(\xi_{n-1})t + f(t_1)f(t - \xi_{n-1})
$$

We continue

$$
\begin{align*}
\int f(t)dt - Q(f) &= \int_a^b f(t)dt - \sum^N h f(\xi_{n-1}) \\
&= \sum^N (\int_{\xi_{n-1}}^{\xi_n} f(t)dt - h f(\xi_{n-1})) \\
&= \sum^N (\int_{\xi_{n-1}}^{\xi_n} f(\xi_{n-1})t + f(t_1)f(t - \xi_{n-1})dt - hf(\xi_{n-1})) \\
&= \sum^N ([tf(\xi_{n-1})]^{\xi_n}_{\xi_{n-1}} + f(\hat{t}_n) [(t - \xi_{n-1})^2 \cdot \frac{1}{2}]^{\xi_n}_{\xi_{n-1}}) \\
&= \sum^N f'(\hat{t}_n) \frac{1}{2}(\xi_n - \xi_{n-1})^2 \\
&\leq \frac{h}{2} sup |f'(t)| \sum^N \frac{b- a}{N} \\
&= \frac{b-a}{2}h sup |f'(t)|
\end{align*}
$$

{{< /details >}}


## Problem 22: Floating Numbers

Given a base \(B \geq 2\), a minimal exponent \(e_{min} \in \mathbb{Z}\) and lengths \(L_m, L_e \in \mathbb{N}\).

(a) Formulate the definition of the set \(FL_+\) of normalized positive floating-point numbers for the given quantities.

(b) Determine \(\max FL_+\) and \(\min FL_+\).

(c) Let \(x \in FL_+\) and let \(y \in FL_+\) be a floating-point number directly adjacent to \(x\). Show that
$$2 \text{ eps } B^{-1} < \frac{|x-y|}{|x|} \leq 2 \text{ eps},$$
where eps is the machine epsilon.

(d) State the advantage of choosing \(B = 2\) with regard to the representation of floating-point numbers and formulate estimates analogous to (c), if this advantage is implemented.


{{< details "Solution a)" "false" >}}

$$
FL_+ = \left\{ B^e \sum_{l=1}^{l_m} a_l B^{-l} \;\Bigg|\;
e = e_{\min} + \sum_{l=0}^{L_e-1} c_l B^l,\;
a_1 \neq 0,\; c_l \in \{0, \dots, B-1\} \right\}
$$

{{< /details >}}

{{< details "Solution b)" "false" >}}

$$
maxFL_+ = B^{e_{max}} (1- B^{-L_m}) = B^{e_{min} + (B-1) \frac{1 - B^{L_e - 1}}{1 - B}} (1 - B^{-L_m}) = (1 - B^{-L_m})B^{e_{{min} + B^{L_e - 1}}}
$$

$$
minFL_+ = B^{-1}B^{e_{min}} = B^{e_{min} - 1}
$$

{{< /details >}}

{{< details "Solution c)" "false" >}}

First

$$
2 eps B^{-1} = 2 \frac{B^{1-L_m}}{2} B^{-1} = B^{1-L_m}B^{-1} = B^{-L_m}
$$

Next

$$
2 eps = \frac{B^{1 - L_m}}{2} = B^{1-L_m}
$$

And let \(x = mB^e\) than is \(y = (m \pm B^{-L_m})B^e\) thus

$$
\frac{|x -y|}{|x|} = \frac{|mB^e - (m \pm B^{-L_m})B^e|}{mB^e} = \frac{B^{-L_m}}{m}
$$

With that we have the inequality.

{{< /details >}}

{{< details "Solution d)" "false" >}}

In the case of \(B = 2\) we don't need to save \(a_1 = 1\). Thus we have an extra bit that we can use for the floating number. Hence the adjucent number \(y = (m \pm B^{-L_m + 1})B^e\).

Then

$$
2 eps = \frac{B^{1 - L_m+1}}{2} = B^{L_m} = eps
$$

And

$$
2 eps B^{-1} = 2 \frac{B^{1-L_m+1}}{2} B^{-1} = B^{1-L_m+1}B^{-1} = B^{-L_m + 1}
$$

{{< /details >}}


## Problem 23: Interpolation Polynomials

Given the table of values:

$$
\begin{array}{|c|c|c|c|c|}
\hline
n & 0 & 1 & 2 & 3 \\
\hline
x_n & -1 & 2 & 4 & 5 \\
\hline
f_n & 3 & -3 & 63 & 99 \\
\hline
\end{array}
$$

(a) Determine the corresponding interpolation polynomial in Newton form.

(b) We add the point \((x_4, f_4) = (0, 59)\) to the nodes above. Determine the corresponding interpolation polynomial.

(c) Let \(p \in \mathbb{P}_N\) be the interpolation polynomial for a continuous function \(f: [a, b] \to \mathbb{R}\) at the pairwise distinct nodes \(x_0, \dots, x_N \in [a, b]\). Let also \(q \in \mathbb{P}_N\) be arbitrary.

(i) First show that
$$\max_{x \in [a,b]} |q(x) - p(x)| \leq \Lambda_N \max_{x \in [a,b]} |q(x) - f(x)|.$$
Give \(\Lambda_N\) explicitly.

(ii) Then show that
$$\max_{x \in [a,b]} |f(x) - p(x)| \leq (1 + \Lambda_N) \max_{x \in [a,b]} |q(x) - f(x)|.$$

(iii) Briefly discuss the statement of the estimate in (ii). In doing so, refer to two different classes of nodes from the lecture for \(N \approx 20\).


{{< details "Solution a)" "false" >}}

We have

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 80%" src="/attachments/numerical_methods/newtonpolynomial_task_23_a.png">
</figure>
{{< /rawhtml >}}

Thus the newton interpolation polynomial is

$$
p_{0,3}(t) = 3 − 2(t + 1) + 7(t + 1)(t − 2) − (t + 1)(t − 2)(t − 4)
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

We have

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 80%" src="/attachments/numerical_methods/newtonpolynomial_task_23_b.png">
</figure>
{{< /rawhtml >}}

Thus the newton interpolation polynomial is

$$
p_{0,4}(t) = p_{0,3}  2(t + 1)(t − 2)(t − 4)(t − 5)
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

(i)
Because p is the polynomial interpolation of f, which means it has the same roots. We have

$$
p(x) = \sum^N p(x_n) L_n(x) = \sum^N f(x_n) L_n(x)
$$

and

$$
q(x) = \sum^N q(x) L_n(x)
$$

Hence

$$
\begin{align*}
\max |q(x) - p(x)| &= \max |\sum^N q(x_n) L_n(x) - \sum^N f(x_n) L_n(x)| \\
&\leq \max \sum |q(x_n)- f(x_n)| |L_n(x)|\\
&\leq \max \sum |L_n(x)| \max_{x \in x_n} |q(x)- f(x)| \\
&\leq \max \Lambda_N |q(x) - f(x)|
\end{align*}
$$

(ii)
We can do

$$
|f (x) − p(x)| = |f (x) − q(x)| + |q(x) − p(x)|
$$

And now we can use (i)

$$
\max|f (x)−p(x)| \leq \max |f (x)−q(x)| + \max |q(x)−p(x)| \leq (1+Λ N ) \max |f (x)−q(x)|.
$$

(iii)
This formula tells us, how good our interpolation polynomial is, the maximum is \((1 + \Lambda_N)\), where \(\Lambda_N\) is the lebesgue constant.

If we choose aquidistant roots, so is the lebesgue constant very big and the approximation is not useful. For Tschebyscheff roots, the lesbesgue constant is near its minima 1, and we get a useful approximation.

{{< /details >}}


## Problem 24: Quadrature Formulas

Let \((b_k, c_k)_{k=1,\dots,s}\) be a quadrature formula of order \(p\).

(a) Formulate the definition of the order as given in the lecture.

(b) Show that if \(p \geq s\), the weights are uniquely determined by the nodes. Give an explicit representation of the weights.

(c) Let \(p \geq s, m \geq 1\) and \(M(x) = (x-c_1) \cdots (x-c_s)\). Show that the order is exactly \(s+m\), if
$$\int_0^1 M(x) g(x) dx = 0$$
for all polynomials \(g \in \mathbb{P}_{m-1}\), but not for one of degree \(m\).
*Hint: Use a representation without proof that could be justified by polynomial division or the Euclidean division algorithm.*

(d) Give the maximum order of the quadrature formula. Justify your answer with the help of subproblem (c).


{{< details "Solution a)" "false" >}}

A a quadrature formula \((b_k, c_k)\) has the order \(p\) if for all polynomials from degree \(\leq p-1\) the integral can be calculated exactly, whereby \(p\) is maximal.

{{< /details >}}


{{< details "Solution b)" "false" >}}

The lagrange Polynomial \(L_n\) arre determinted through the knots \(c_1, .., c_s\). For the order \(p \geq s\), follows with \(L_j(c_k) = \delta_{jk}\)

$$
\int_0^1 L_j(x) dx = \sum^s b_k L_j(ck) = b_j
$$

{{< /details >}}

{{< details "Solution c)" "false" >}}

Let \(f \in \mathbb{P}_{s + m - 1}\) be arbitrarily. Then exist a polynomial \(g \in \mathbb{P}_{m-1}\) and \(r \in \mathbb{P}_{s-1}\) with \(f = Mg + r\) because of polynomial division.

And

$$
\int f(x) dx = \int M(g)g(x) fx + \int r(x) dx
$$

and the same for their interpolation

$$
\sum b_k f(c_k) = \sum b_k M(c_k)g(c_k) + \su b_k r_k(c_k)
$$

And because \(p \geq s\) the last summands of both formulas are the same. Hence the polynomical inteprolcation calculates the exact integral.

Fro mthis follows that the order is exactly then \(m +s\) when

$$
\int M(x)g(x) dx = 0
$$

for all polynomials of order \(\leqm-1\), but not for ones of order \(m\).

{{< /details >}}

{{< details "Solution d)" "false" >}}

The maximum order we can have is \(2s\) because that would mean that we have \(g = M\) and then

$$
\int M(x)g(x) dx = \int M(x)^2 dx > 0
$$

{{< /details >}}



## Problem 25: Matrices


{{< details "Solution a)" "false" >}}

We have \(||A|| = \sup  \frac{||Ax||}{||x||} = \max ||Ax||\). Hence

$$
||AB|| = \max ||ABx|| \leq \max ||A|| ||Bx|| = ||A|| \max ||Bx|| = ||A||||B||
$$


{{< /details >}}


{{< details "Solution b)" "false" >}}

We have

$$
1 = ||I_n|| = ||A^{-1}A|| \leq ||A^{-1}||||A|| = cond(A)
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

Because \(Ax=b\) we can rwrite

$$
x - \hat{x} = A^{-1}b - A^{-1}\hat{b}
$$

Thus

$$
||x- \hat{x}|| = ||A^{-1}(b - \hat{b})|| \leq ||A^{-1}||||b - \hat{b}||
$$

And with that

$$
\frac{||x - \hat{x}||}{||x||} \leq \frac{||A^{-1}||||b - \hat{b}||}{||x||} = \frac{||b||||A^{-1}||||b - \hat{b}||}{||x||||b||} = \frac{||b||||A^{-1}||}{||x||}\frac{||b - \hat{b}||}{||b||} \leq ||A||||A^{-1}|| \frac{||b - \hat{b}||}{||b||}
$$

For this approximation to be useful the error of \(|| \frac{||b - \hat{b}||/||b||\) needs to be small.

If our condition number is small this approximation guarantees, that small errors in \(b\) lead to small innacuracies from \(x\).
Is the condition number nig, so can even a small error lead to a big error in our solution, but it doesnt have to be, because the right side of the approximation is so loose.

{{< /details >}}


{{< details "Solution d)" "false" >}}

Because \(e \neq 0\), is \(ee^T\) a Matrix with rang 1. Hence 0 is a eigenvalue with the multiplicity of \(N-1\).

Next, \(Kern(ee^T) = \orth \span{e}\).

In addition we have the eigenvalue \(N > 0\) because \(ee^Te = e^Tee = Ne\). With that we have the spectrum.

Next with \(ev^Tve^T = ||v||_2^2ee^T\) we get

$$
||ve^T||_2 = \sqrt{\max{\lambda \in ev^Tve^T}} = ||v||_2 \sqrt{\max{\lambda \in ee^T}} = ||v||_2 \sqrt{N}
$$

{{< /details >}}



## Problem 26: CG-Algorithm


{{< details "Solution a)" "false" >}}

We have \(\phi(x) = \frac{1}{2}x^TAx - x^Tb\), which gets minimized by the CG-Algorithm.

A necessary condition for the minima \(x^*\) is that \(\phi(x^*) = (Ax^* -b)^T = 0^T\). This condition is because of \(\phi''(x) = A\) symmetrical and positiv deifnit also sufficient.

Hence is \(x^*\) then the minima from \(\phi\), if \(x^*\) solves the LGS \(Ax = b\).

{{< /details >}}
