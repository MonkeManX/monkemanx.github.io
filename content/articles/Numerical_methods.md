---
title: 'Numerical Methods for Computer Scientist'
date: 2025-05-04 09:00:00
tags: ["Mathematics"]
draft: True
---

{{< Info "Info" >}}

This is a summary of the Lecture at the KIT *Numerische Mathematik für die Fachrichtungen Informatik*, as such is not one body of text but more like choppy notes.

{{< /Info >}}

## 1. Floating point calculation, error source, conditions and stability

### 1.1 Floating point calculation 

**Example:**
You can calculate \(\pi\) from the circumference of a circle by drawing several triangles inside it.

{{< rawhtml >}}
<figure>
<img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 50%" src="/attachments/numerical_methods/calculate_pi_circle.jpg">
</figure>
{{< /rawhtml >}}

We can make the following observations:
1. \(g_6 = r\) (equilateral triangles),
2. \(r^2 = h^2_n + (g_n/2)^2\) (Pythagoras),
3. \(g^2_{2n} = (r - h_n)^2 + (g_n/2)^2\) (Pythagoras).

Form this we get the rescurcive formula: 
$$
g_{2n} = \sqrt{2 - \sqrt{4 - g_n^2}}
$$

{{< rawhtml >}}
<figure>
<img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 80%" src="/attachments/numerical_methods/instability_pi_calculation.jpg">
</figure>
{{< /rawhtml >}}

What you see here is that if you use too many triangles, the approximation of \(\pi\) doesn't become more accurate, but less accurate, until the error reaches a maximum.

Another recursive formula, we can get by reorganizing the terms, that is numerically more stable is the following:

$$
g_{2n} = \frac{g_{n}}{\sqrt{2 + \sqrt{4 - g_{n}^2}}}
$$

Using this formula the \(\pi\) caculation is significantly more stable.

{{< rawhtml >}}
<figure>
<img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 80%" src="/attachments/numerical_methods/pi_stabble_clauclation.jpg">
</figure>
{{< /rawhtml >}}



### 1.2 Normalized floating point numbers

In computers, numbers are represented as:

$$
m \cdot B^e
$$

where the fixed base \(B \in \mathbb{N} \setminus \{1\}\), typically \(B = 2\), and the exponent \(e \in [e_{\text{min}}, e_{\text{max}}] \cap \mathbb{Z}\) is an integer given by:

$$
e = e_{\text{min}} + \sum_{l=0}^{L_e - 1} c_l B^l
$$

We need \(e_{\text{min}}\) because otherwise the exponent would be entirely positive, and we want to allow negative exponents as well.

The *mantissa* \(m\) is either 0 or a number in the range \(B^{-1} \leq |m| < 1\), and has the form:

$$
m = \pm \sum_{l = 1}^{L_m} a_l B^{-l}, a_1 \neq 0
$$

where \(L_m\) denotes the mantissa length. The condition \(a_1 \neq 0\), which is equivalent to \(B^{-1} \leq |m|\), defines **normalization** and thus ensures uniqueness of the representation.

**Example**
For the decimal number 10.75:

$$
0.10750 \cdot 10^2 \quad \text{for } B = 10, \ e = 2, \ L_m = 5
$$

> **Definition** (The set of normalized floating-point numbers):  
> Let \(B \geq 2, e_{\text{min}}\), and the lengths \(L_m, L_e\) be given. We define the set
> 
> $$
FL := FL_{-} \cup \{0\} \cup FL_{+}
$$
> 
> of floating-point numbers as:
> 
> $$
FL_{+} := \left\{B^{e} \sum_{l=1}^{L_m} a_l B^{-l} : e = e_{\text{min}} + \sum_{l=0}^{L_e - 1} c_l B^{l}, \ a_l, c_l \in \{0, \dots, B-1\}, \ a_1 \neq 0 \right\}
$$
> 
> and \(FL_{-}\) is the mirrored set of negative numbers.

**Consequences:**  
- \(FL \subset \mathbb{Q}, |FL| < \infty \)
- \(e_{\text{max}} = e_{\text{min}} + B^{L_e} - 1\)
- \(\max FL = -\min FL = B^{e_{\text{max}}}(1 - B^{-L_m})\)
- \(\min FL_{+} = B^{e_{\text{min}} - 1}\)

Thus, every real number \(x \in \mathbb{R}\) can be represented approximately as a floating-point number \(fl(x)\) after rounding:

$$
x = \pm B^e \sum_{l=1}^{\infty} a_l B^{-l}, \quad \text{with } a_1 \neq 0
$$

We define:

$$
fl(x) = \pm B^e \cdot
\begin{cases}
\sum\limits_{l=1}^{L_m} a_l B^{-l} & \text{if } a_{L_m + 1} < B/2 \\
\sum\limits_{l=1}^{L_m} a_l B^{-l} + B^{-L_m} & \text{if } a_{L_m + 1} \geq B/2
\end{cases}
$$

For the relative error of \(fl(x)\):

$$
\frac{|x - fl(x|)}{|x|} \leq \frac{B}{2} B^{-L_m} = \frac{B^{(1 -L_m)}}{2} =: eps
$$

We note:
- \(B^{-(L_m + 1)}\) is the position where digits are truncated.
- \(B/2\) is the maximum rounding error possible for a single digit.

This means we must scale the digit error by the position at which it occurs.

This is equivalent to:

$$
fl(x) = x(1 + \epsilon), \quad \text{with } |\epsilon| \leq \text{eps}
$$


### 1.3 Floating point arithmetic

The result of an arithmetic operation does not have to be a floating-point number, even if \(x\) and \(y\) are.

We define the floating-point operation \(\bullet \in \{+, -, \cdot, / \}\):

$$
x \hat{\bullet} y := fl(x \bullet y)
$$

It holds that:

$$
x \hat{\bullet} y = (x \bullet y)(1 + \epsilon)
$$

*Remarks:*  
- The floating-point operation does not have to be associative.
- For \(y \in FL\), it holds that: \(1 \hat{+} y = 1\), if \(|a| \le \epsilon\).
- For \(B=2\), normalized floating-point numbers do not need to store the first decimal place since it is 1.


### 1.4 Sources of Error

Schema:
Input Data → Algorithm → Result

Depending on the algorithm, the result may only be an approximation.
This leads to *approximation errors*.
Another source of error is *rounding errors due to floating-point arithmetic*.

All of this is encompassed in the **stability of the algorithm**.

There can also be disturbances in the input data, which is called the *condition of the problem*.

In total, there are the following errors:

- Input errors
- Rounding errors
- Approximation errors
- Discretization errors
- Error amplification


## 1.5 Condition of a Problem

Errors in input data → Optimal solution method → Errors in the solution.

Condition of the problem:

- How do errors in the input data affect the result?
- A measure of the dependence of the solution on the data
- A measure of the unavoidable error amplification

*Example:*
We want to solve the LGS \(Ax = b\) with the error \(\epsilon\)

$$
A = 
\begin{pmatrix}
1 & 1 \\
1 & 1 - \epsilon
\end{pmatrix}, \
b = 
\begin{pmatrix}
4 \\
4 - \epsilon
\end{pmatrix}, \ 
x =
\begin{pmatrix}
3 \\
1
\end{pmatrix}
$$

Do we now change \(b\) then we get a solution

$$
b = 
\begin{pmatrix}
4 + \epsilon \\
4 - 2\epsilon
\end{pmatrix}, \ 
x =
\begin{pmatrix}
1 + \epsilon \\
3
\end{pmatrix}
$$

This means small erros in input data \(b\), lead to big changs in our solution. The LGS badly conditioned.


## 1.6 Stability of an Algorithm

We call a numerical procedure stable if the errors within the procedure are "not much larger" than the impact of disturbances in the input data, which are unavoidable.


Stable: The effect of errors has little impact on the result.

*Example:*
Let \(\hat{x} = x(1+ \epsilon_x), \ \hat{y} = y (1 + \epsilon_y)\). It holds that, for the operation \(\bullet \in \{+, -, \cdot, / \}\):

$$
\frac{|x \hat{\bullet} y - (x \bullet y)|}{|x \bullet y|} = |\epsilon| \leq eps
$$

Thus, if \(x, y\) have the same sign, the denominator cancels out, leading to a well-conditioned case.
However, if \(x \approx -y\), we have error amplification due to cancellation, because we have a very small number in the denominator, causing the entire fraction to become very large.

*Note:*
This is the same principle explaining why the \(\pi\) approximation is not stable.



## 2. LR Decomposition for LGS

### 2.1 Quadratic Linear Systems of Equations

**Problem** Given a regular matirx A and a vector b, we want to find a vector x such that
$$
Ax = b
$$

*Remarks:*
- The most important problem in numerical mathematics.
- There is a unique solution \(x^* = A^{-1} b\) because the matrix is regular.
- We use Gaussian elimination to calculate the LR decomposition.


### 2.2 Idea of LR Decomposition

If we find an LR decomposition, then the matrix A is regular, and thus there is a unique solution for the linear system of equations.

1. Calculate \(A = LR\) with \(L, R \in \mathbb{R}^{n \times n}\).
2. Solve \(Ly = b\) via forward substitution:
   \(y_1 = \frac{b_1}{l_{11}}, \quad y_2 = \frac{b_2 - l_{21} \cdot y_1}{l_{22}}, \quad \dots\)
3. Solve \(Rx = y\) via backward substitution:
   \(x_n = \frac{y_n}{r_{nn}}, \quad \dots\)
4. Then we have the solution, since \(A x = L R x = L y = y\).

If \(\det A \neq 0\), then \(\det L \neq 0\) and $\det R \neq 0\).

### 2.3 Complexity of LR Decomposition

Both forward and backward substitution have a complexity of \(\frac{1}{2} N^2\) operations.
Here, *1 operation* = *1 multiplication and 1 addition*.

Python implementation:

```py
import numpy as np

def backward_sub(R, y):
    N = len(y)
    x = np.zeros(N)
    for n in range(N-1, -1, -1): # n = N-1,...,0
        x[n] = (y[n] - np.dot(R[n,n:N], x[n:N])) / R[n,n]
    return x
```

Calculating the matrix-vector multiplication \(x^* = A^{-1}b\) costs \(N^2\) **operations**.

Performing both forward and backward substitution costs \(N^2\) **operations**.

**Conclusion:** Knowing \(A^{-1}\) brings no advantage.


### 2.4 Definition and Theorem

With the normalization \(l_{nn} = 1\) in LR, it means that only 1's are on the main diagonal. This makes the \(L\) matrix unique; otherwise, we could shift the diagonal values to the \(R\) matrix.

**Lemma**
> It exists exactly one LR-decomposition from A of the form A = LR, if and only if all its sub-main-matrices are invertible. This decomposition is unique and an be calculatd in \(1/3 N^3\) operations.

The LR-deocmposition is:

$$
R :=
\begin{pmatrix}
R_{11} & r_{12} \\
0^T_n & r_{22}
\end{pmatrix}, \
L :=
\begin{pmatrix}
L_{11} & 0_n \\
l_{21}^T & 1
\end{pmatrix}
$$

with

$$
r_{12} = L_{11}^{-1} a_{12}
$$

**Example:**

![](/attachments/numerical_methods/2024-04-19-19-39-15.png)
![](/attachments/numerical_methods/2024-04-19-19-39-23.png)
![](/attachments/numerical_methods/2024-04-19-19-39-31.png)


### 2.5 LR Decomposition with Permutation

> **Lemma**
> Let A be regular. Then exist a permuations matrix P, with that PA the requirements of the LR-decomposition fullfills. 

This means that after permuting the rows of our matrix, an LR decomposition exists.

**Plan**
It holds that: \(A x = b \iff P A = P b\).

1. Calculate \(P A = LR\).
2. Solve \(Ly = P b\).
3. Solve \(R x = y\).

*Remarks:*
- L and R can be stored in the matrix A.
- The pivot choice is made during the computation in practice.

**Example (with pivoting):**

![](/attachments/numerical_methods/example_LU_decomposition_pivot.jpg)

*Notes*: 
- The vector at the start describes the pivot choice, initially just numbered in order starting from 1.
- You first go to the first column and decide which row should be taken as the top one to eliminate the others, and you should choose the row with the largest element in absolute value.
- The factors (written in red) for row elimination are stored in the matrix, but they do not belong to the matrix itself; they are just kept for reference.



## 3. Cholesky and QR Decomposition

### 3.1 Cholesky Decomposition

#### 3.1.1 Problem Statement

We have a matrix that we want to decompose in order to solve a system of linear equations (SLE) more easily.  
**Problem:** \(Ax = b\)    
**Given:** \(A \in \mathbb{R}^{N \times N}\), SPD matrix, \(b \in \mathbb{R}^n\)   
**Find:** \(x \in \mathbb{R}^n\)  

#### 3.1.2 Recap: Symmetric, Positive Definite

SPD = symmetric + positive definite.

- A is symmetric: \(A = A^T\)
- A is positive definite: \(x^T A x > 0,\ x \neq 0\)

#### 3.1.3 Idea of the Cholesky Decomposition

1. Compute decomposition: \(A = L \cdot L^T\), with L a regular lower triangular matrix.
2. Solve \(Ly = b\) using forward substitution
3. Solve \(L^T x = y\) using back substitution

Then \(x\) is the solution, since:
\(Ax = L \cdot L^T x = Ly = b\)

#### 3.1.4 Computation of the Cholesky Decomposition

**Theorem**

> Let A be regular. Then A has a Cholesky decomposition \(A = L \cdot L^T\) if and only if \(A\) is SPD, i.e., symmetric and positive definite.

**Proof:**
“\(\Rightarrow\)” Assume \(A = L \cdot L^T\) with L regular.

$$
A^T = (L \cdot L^T)^T = (L^T)^T \cdot L^T = L \cdot L^T = A
$$
⇒ Symmetric

$$
x^T A x = x^T L L^T x = (L^T x)^T L^T x = y^T y, \text{ with } y := L^T x
$$
⇒ \(y^T y = \|y\|^2\), which is always positive and non-zero since the matrix is regular (trivial kernel) and \(x \neq 0\)

“\(\Leftarrow\)” Use induction

(Base case) N = 1, i.e., a 1x1 matrix.
$$
a_{11} = \sqrt{a_{11}} \cdot \sqrt{a_{11}}
$$

(Inductive Step) \(n \rightarrow n+1\)


Since the matrix is symmetric, the vector \(a_{21}\) must appear symmetrically (i.e., transposed) above and below.

The symmetry of the whole matrix carries over to the submatrix \(A_{11}\):
$$
y^T A_{11} y = (y^T, 0) A (y, 0)^T > 0
$$
We extend the vector y with a 0, so that the product with A matches the same result as before.

⇒ \(A_{11}\) is SPD.

So by the induction hypothesis, \(A_{11}\) has a Cholesky decomposition:
$$
A_{11} = L_{11} L_{11}^T
$$

**Approach:**

We obtain the following equations:

1. \(L_{11} \cdot l_{21} = a_{21}\)
2. \(l_{21}^T \cdot l_{21} + l_{22}^2 = a_{22}\)

To solve (1), we can use forward substitution for \(l_{21}\).
For (2):

#### 3.1.5 Computational Cost of Cholesky Decomposition

Cost of forward substitution: \(\sum \frac{1}{2} n^2 = \frac{1}{2} \sum n^2 \approx \frac{1}{6} N^3\)

**Note:** LU decomposition requires roughly twice the computational effort.

#### 3.1.6 The Algorithm

**Input:** A, or just the lower or upper triangular part (since A is symmetric)  
**Output:** Cholesky decomposition L  

**Algorithm:**

1. \(L[1,1] = \sqrt{A[1,1]}\)
2. For n = 2, ..., N:
- Solve \(L[1:n-1,1:n-1]y = A[1:n-1,n]\quad (= A[n,1:n-1]^T)\)
- Set \(L[n,1:n-1] = y^T\)
- Compute \(L[n,n] = \sqrt{A[n,n] - y^T y}\)

#### 3.1.7 Remarks

1. L can be stored directly in matrix A
2. One can numerically check whether A is SPD by attempting the Cholesky algorithm. If a decomposition is successful, the matrix is symmetric.

**Summary:**
Cholesky is twice as fast as LU decomposition but requires more structure (i.e., SPD matrices).


### 3.2 QR Decomposition

#### 3.2.1 Problem Statement

**Problem:** \(Ax = b\)    
**Given:** \(A \in \mathbb{R}^{m \times n}\), with \(m \geq n\), and \(b \in \mathbb{R}^m\)  
**Find:** \(x \in \mathbb{R}^n\)   

So, the matrix no longer needs to be square.

We decompose our matrix A as follows:

$$
A = Q \cdot R, \quad \text{with orthogonal matrix } Q \in \mathbb{R}^{m \times m} \text{ (i.e., } Q^T Q = Q Q^T = I\text{)}
$$


#### 3.2.2 Idea of the QR Decomposition

To solve \(Ax = b\), assuming the system is solvable (unlike Cholesky and LU, solvability is not guaranteed here):

1. Compute the QR decomposition \(A = Q R\)
2. Solve \(Qc = b \Rightarrow c = Q^T b\) (requires \(M^2\) operations)
3. Solve \(Rx = c\) via back substitution

Then x is a solution:

$$
Ax = QRx = Qc = b
$$

#### 3.2.3 Householder Transformations

Let \(v \in \mathbb{R}^m,\ v \neq 0\). We seek a matrix \(Q = I - 2ww^T\), with \(w \in \mathbb{R}^m\) and \()\|w\|_2^2 = 1\), such that:

$$
Qv = \sigma e_1
$$

We want to reflect an arbitrary vector $v$ onto a multiple of the unit vector \(e_1\).

**Observations:**

1. Q is symmetric:

   $$
   Q^T = I^T - 2(w^T)^T w^T = I - 2ww^T = Q
   $$
2. Q is orthogonal:

   $$
   QQ^T = Q^T Q = Q^2 = (I - 2ww^T)^2 = I - 4ww^T + 4ww^T ww^T = I
   $$
3. Q is a reflection:

   $$
   Qw = w - 2ww^T w = -w
   $$

Since Q is orthogonal, it preserves vector norms:

$$
\|Qx\|_2 = \|x\|_2
$$

We want to reflect vector v to get \(Qv = \sigma e_1\).
Then:

$$
\|v\|_2 = \|Qv\|_2 = \|\sigma e_1\|_2 = |\sigma|
$$

The sign of \(\sigma\) can be chosen to avoid **cancellation** errors.

**Computation of w (and \(\sigma\):**

- Case \(v_1 > 0\): set \(\sigma = -\|v\|_2\)
- Case \(v_1 \leq 0\): set \(\sigma = \|v\|_2\)

Then define:

$$
w = \frac{v - \sigma e_1}{\|v - \sigma e_1\|_2}
$$

This distinction avoids subtracting numbers of the same sign (which can lead to loss of significance), and instead encourages operations where signs differ (more numerically stable).


The black vector v is reflected to align with either of the black or blue directions shown. The circle represents the norm of v; Householder preserves the length, so the result must also lie on the circle. The red line shows all vectors orthogonal to w.

#### 3.2.4 Computing the QR Decomposition

**Theorem**

> For every matrix \(A \in \mathbb{R}^{m \times n},\ m \geq n\), of full rank (to ensure a unique solution), a QR decomposition exists.

**Proof** (by induction on n):

**Base case (n = 1):**
Then A is a column vector. Use a Householder transformation to reflect this vector onto a multiple of the unit vector.

Let \(a^{(1)} \in \mathbb{R}^m\) be the first column of A. Define \(Q_1 = I - 2w_1 w_1^T\) such that:

$$
Q_1 a^{(1)} = r_{11} e_1,\quad \text{where } r_{11} = \sigma
$$


**Note:**
You never need to explicitly compute the full matrix Q; it can be applied directly:

$$
(I - 2w_1 w_1^T) a^{(j)} = a^{(j)} - 2 w_1^T a^{(j)} \cdot w_1
$$

Cost: 2m operations per column.
Total cost for computing all \(r_{1j}\) and updating \(A^{(1)}: 2m(n - 1)\)



## Solutions Not Checked Yet



## Solutions Checked

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
&= \max \ E^- + \sum_{k=0}^{E - 1} c_k B^{k} \\
&= E^- + (B - 1) \sum_{k=0}^{E - 1}  B^{k} \\
&= E^- + (B-1) \frac{B^{E - 1} -1}{B -1} \\
&= E^- + B^{E-1} - 1
\end{align*}
$$

(ii)

$$
\begin{align*}
|m| &= |\sum_{l = 1}^{M} a_l B^{-l}| \\
&\leq (B-1) \sum_{l = 1}^{M} B^{-l} \\
&= (B-1) \sum_{l = 0}^{M} B^{-1} B^{-l} \\
&= \frac{(B - 1)}{B} \frac{1 - B^{-M}}{1 - B^{-1}} \\
&= 1 - B^{-M} \\
&\le 1
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


{{< rawhtml >}}
<figure>
<img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width: 90%" src="/attachments/numerical_methods/nummerical_methods_task1b_tasksheet1.jpg">
</figure>

{{< /rawhtml >}}


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

We have:

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

We have:

$$
A = \begin{pmatrix}
\alpha & 1 \\
 1 & 0
\end{pmatrix}, \quad 
L = \begin{pmatrix}
1 & 0 \\
1/\alpha & 1
\end{pmatrix}, \quad 
R = \begin{pmatrix}
\alpha & 1 \\
 0 & -1/\alpha
\end{pmatrix}, \quad 
$$

To get the condition we caluclate 

$$
cond(A) = ||A|| \cdot ||A^{-1} ||
$$

We caluclate the inverses:

$$
A^{-1} = \begin{pmatrix}
0 & -1 \\
-1 & -\alpha
\end{pmatrix}, \quad 
L^{-1} = \begin{pmatrix}
1 & 0 \\
-1/\alpha & 1
\end{pmatrix}, \quad 
R^{-1} = \begin{pmatrix}
-1/\alpha & -1 \\
 0 & alpha
\end{pmatrix}, \quad 
$$

Thus for A we get

$$
cond(A)_1 = (1 + K)^2\quad
cond(A)_\infty = (1 + K)^2\quad
cond(A)_F =2 + \alpha^2 
$$

For L we get 

$$
cond(L)_1 = (1 + 1/\alpha)^2\quad
cond(L)_\infty = (1 + 1/\alpha)^2\quad
cond(L)_F = 2 + 1/\alpha^2
$$

For U we get

$$
cond(U)_1 = / \quad
cond(U)_\infty = / \quad
cond(U)_F = 1 +\alpha^2 + 1/\alpha^2
$$

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
