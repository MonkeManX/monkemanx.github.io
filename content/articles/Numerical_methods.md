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



### Problem 3: QR-Decomposition

Calculate the QR decomposition for

$$A = \begin{pmatrix} 1 & 2 \\ 1 & 2 \\ \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \end{pmatrix}.$$

State all Householder transformations \(Q\) used.


{{< details "Solution" "false" >}}

{{< info "Recap QR-Decomposition" >}}

The prerequiste for the QR Decompostion is a matrix A with maximum Rank. The decomposition is then \(A = QR\) with \(Q\) being a ortihogonal matrix \(R = \begin{pmatrix}\hat{R} \\ 0 \end{pmatrix}\) and \(\hat{R}\) a top triangular matrix.

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

And calculate the hoouseholder vector

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

We now caluclate the matrix \(Q_1\)

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

Now we can do the second column, rmember to get to this we need to remvoe the first column and the first row of \(Q_1 A\) which we jsut cualcuated

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

Thsu we get

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
The prerequisite for choelsky deocmpsoiton to work is that our matrix \(A\) is symmetrical and positive definite. The decomposition is then \(A = l \cdot L^T\) with \(L\) a regular lowere triangular matrix.

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

The first case, in the formula, is for the upper orner of the triangular matrix which jsut has 0 entries.
The second case, is for the diagonal from the top left orner to the bottom right corner, what we do here is we take the square root from the entry \(a_{kk}\) that leis on the \(A\) martix on the diagonal and from it we subrtact the squared sum of all entires in the same row from the current \(L\) martix, aftert that we take the squrae root form it.
The thrid case is for all the entries in the lower half on the matrix that are not on the diagonal, what we do here is we take the current enrty\(a_{ik}\) from oru Matrix \(A\) and fro mti subtract the sum from the entris that came before in the same row multipleid with the entries of the same column divided by teh diagonal entry \(l_{kk}\) fro mthe Current matrix \(L\).

An exmaple is in order:

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

We want ot cualcuate its choleky decompsoition. For this we simply follow the algorithm as laid out prior:

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

A is symmetric thsu we only need to calculate half of the matrix entries, thsu we have 1/2(N^2 + N) entries co culate the +N we have because we also need to clauclate the diagonal.
Ad for eah etry we need to make a facotres sum of m entires thus we have, \((N^2 + N)\cdot M\) oepration

For the choleksy deocmpsotion we need \((1/3 N^3)\) Operation.

Thus i ntoal to clauclate we need \(N^2(M + \frac{1}{3}N) + N \cdot M\) Operations.

{{< /details >}}


{{< details "Solution c)" "false" >}}

So we have \(B = QR\), with \(Q\) ebing orthogonal, and want a cholesky decomposition \(A = LL^T\).

Thus

$$
A = B^TB = (QR)^TQR = R^TQ^TQR = R^TR
$$

Where \(R = \begin{pmatrix} \hat{R} \\ 0 \end{pmatrix}\) and \(\hat{R}\) is a upper triangular matrix.

Hence we can set \(L = \hat{R}^T\) to get a cholesky deomposition from a QR decomposition.

{{< /details >}}


{{< details "Solution d)" "false" >}}

The complexity of (b) is \(N^2(M + \frac{1}{3}N)\).

The compelxity of QR-Algorithm is \(2N^2(M - \frac{1}{3}N)\)

Now in the case of (c), if \(N < M\) then the complexity is approximately teh same. But if \(M >> N\) then QR is much more expensive.

{{< /details >}}
