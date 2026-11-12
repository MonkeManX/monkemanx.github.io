---
title: 'Excersises for Robotics'
date: 2026-11-09 16:00:00
tags: ["Robotics"]
draft: True
---

The following is a sheet of robotics excersises and their solutions. It is a mix of problems taken from old exams and practice sheets from the [KIT](https://www.kit.edu/english/) *"[Robotics I - Introduction to Robotics](https://h2t.iar.kit.edu/1967.php)"* lecture.


## Excersises with Confirmed Solution

This section contains only problems with official solutions.

### Exercise 1 (Euler Angles)

Let \(R_1\) be a general \(3 \times 3\) rotation matrix,  

$$
R_1 =
\begin{pmatrix}
n_x & o_x & a_x \\
n_y & o_y & a_y \\
n_z & o_z & a_z
\end{pmatrix}
$$

i.) Calculate the Euler angles \(zx'z''\) corresponding to \(R_1\).

ii.) Calculate the fixed angles (xyz convention) corresponding to \(R_1\).

{{< details "Solution a)" "false" >}}

In Euler angles with \(zx'z'''\) convention, we first rotate around the z-axis, then around the x-axis, and finally around the z-axis again. Hence, we can represent this sequence using three rotation matrices.


$$
\begin{aligned}
\begin{pmatrix}
n_x & o_x & a_x \\
n_y & o_y & a_y \\
n_z & o_z & a_z
\end{pmatrix}
&=
\begin{pmatrix}
c_\alpha & -s_\alpha & 0 \\
s_\alpha & c_\alpha & 0 \\
0 & 0 & 1
\end{pmatrix}
\cdot
\begin{pmatrix}
1 & 0 & 0 \\
0 & c_\beta & -s_\beta \\
0 & s_\beta & c_\beta
\end{pmatrix}
\cdot
\begin{pmatrix}
c_\gamma & -s_\gamma & 0 \\
s_\gamma & c_\gamma & 0 \\
0 & 0 & 1
\end{pmatrix}
\\
&=
\begin{pmatrix}
c_\alpha c_\gamma - s_\alpha c_\beta s_\gamma &
-c_\alpha s_\gamma - s_\alpha c_\beta c_\gamma &
s_\alpha s_\beta \\
s_\alpha c_\gamma + c_\alpha c_\beta s_\gamma &
-s_\alpha s_\gamma + c_\alpha c_\beta c_\gamma &
-c_\alpha s_\beta \\
s_\beta s_\gamma &
s_\beta c_\gamma &
c_\beta
\end{pmatrix}
\end{aligned}
$$

If we comparer the coefficients we can see 

$$
\begin{aligned}
a_z &= \cos(\beta), \\
n_z &= \sin(\beta)\sin(\gamma), \\
o_z &= \sin(\beta)\cos(\gamma), \\
a_x &= \sin(\beta)\sin(\alpha), \\
-a_y &= \sin(\beta)\cos(\alpha).
\end{aligned}
$$

From this follows 

$$
\begin{aligned}
\beta &= \arccos(a_z)
\\[8pt]
\frac{a_x}{-a_y}
&= \frac{s_\alpha \cdot s_\beta}{-c_\alpha \cdot s_\beta}
= -\frac{\sin\alpha}{\cos\alpha}
= -\tan\alpha
\\[8pt]
\Rightarrow \quad
\alpha &= \arctan\left(-\frac{a_x}{a_y}\right)
\quad (+180^\circ \text{ if } a_y > 0)
\\[8pt]
\frac{n_z}{o_z}
&= \frac{s_\beta \cdot s_\gamma}{s_\beta \cdot c_\gamma}
= \frac{\sin\gamma}{\cos\gamma}
= \tan\gamma
\\[8pt]
\Rightarrow \quad
\gamma &= \arctan\left(\frac{n_z}{o_z}\right)
\quad (+180^\circ \text{ if } o_z < 0)
\end{aligned}
$$

Hence 

$$
\begin{aligned}
\alpha &= \arctan\left(-\frac{a_x}{a_y}\right)
\quad (+180^\circ \text{ if } a_y > 0)
\\
\beta &= \arccos(a_z)
\\
\gamma &= \arctan\left(\frac{n_z}{o_z}\right)
\quad (+180^\circ \text{ if } o_z < 0)
\end{aligned}
$$

**Assumption:** sin 𝛽 ≠ 0, i.e., 𝛽 ∉ 0°, 180° otherwise the axes coincide and only the sum or difference of 𝛼 and 𝛾 can be determined (one angle free).

{{< /details >}}



{{< details "Solution b)" "false" >}}

In Euler angles with \(xyz\) convention, we first rotate around the x-axis, then around theyx-axis, and finally around the z-axis. Hence, we can represent this sequence using three rotation matrices.

$$
\begin{aligned}
\begin{pmatrix}
n_x & o_x & a_x \\
n_y & o_y & a_y \\
n_z & o_z & a_z
\end{pmatrix}
&=
\begin{pmatrix}
c_\gamma & -s_\gamma & 0 \\
s_\gamma & c_\gamma & 0 \\
0 & 0 & 1
\end{pmatrix}
\cdot
\begin{pmatrix}
c_\beta & 0 & s_\beta \\
0 & 1 & 0 \\
-s_\beta & 0 & c_\beta
\end{pmatrix}
\cdot
\begin{pmatrix}
1 & 0 & 0 \\
0 & c_\alpha & -s_\alpha \\
0 & s_\alpha & c_\alpha
\end{pmatrix}
\\
&=
\begin{pmatrix}
c_\beta c_\gamma &
s_\alpha s_\beta c_\gamma - c_\alpha s_\gamma &
s_\alpha s_\gamma + c_\alpha s_\beta c_\gamma
\\
c_\beta s_\gamma &
s_\alpha s_\beta s_\gamma + c_\alpha c_\gamma &
c_\alpha s_\beta s_\gamma - s_\alpha c_\gamma
\\
-s_\beta &
s_\alpha c_\beta &
c_\alpha c_\beta
\end{pmatrix}
\end{aligned}
$$

If we comparer the coefficients we can see 

$$
\begin{aligned}
n_z &= -\sin(\beta), \\
o_z &= \cos(\beta)\sin(\alpha), \\
a_z &= \cos(\beta)\cos(\alpha), \\
n_y &= \cos(\beta)\sin(\gamma), \\
n_x &= \cos(\beta)\cos(\gamma).
\end{aligned}
$$

From this follows 

$$
\begin{aligned}
\beta &= \arcsin(-n_z)
\\[8pt]
\frac{o_z}{a_z}
&= \frac{s_\alpha \cdot c_\beta}{c_\alpha \cdot c_\beta}
= \frac{\sin\alpha}{\cos\alpha}
= \tan\alpha
\\[8pt]
\Rightarrow \quad
\alpha &= \arctan\left(\frac{o_z}{a_z}\right)
\quad (+180^\circ \text{ if } a_z < 0)
\\[8pt]
\frac{n_y}{n_x}
&= \frac{c_\beta \cdot s_\gamma}{c_\beta \cdot c_\gamma}
= \frac{\sin\gamma}{\cos\gamma}
= \tan\gamma
\\[8pt]
\Rightarrow \quad
\gamma &= \arctan\left(\frac{n_y}{n_x}\right)
\quad (+180^\circ \text{ if } n_x < 0)
\end{aligned}
$$

Hence 

$$
\begin{aligned}
\alpha &= \arctan\left(\frac{o_z}{a_z}\right)
\quad (+180^\circ \text{ if } a_z < 0)
\\
\beta &= \arcsin(-n_z)
\\
\gamma &= \arctan\left(\frac{n_y}{n_x}\right)
\quad (+180^\circ \text{ if } n_x < 0)
\end{aligned}
$$


**Assumption:** cos 𝛽 ≠ 0, i.e., 𝛽 ≠ ±90° otherwise the axes coincide and only the sum or difference of 𝛼 and 𝛾 can be determined (one angle free).

{{< /details >}}



### Exercise 2 (Rotation Matrix)

Let \(R_2\) be a rotation matrix, given by

$$
R_2 =
\begin{pmatrix}
0.36 & 0.48 & -0.8 \\
-0.8 & 0.6 & 0.0 \\
0.48 & 0.64 & 0.6
\end{pmatrix}
$$

Calculate the quaternion $q$ that describes the rotation given by \(R_2\).

{{< details "Solution" "false" >}}

**Recall:** quaternions is defined as 

$$
\mathbf{q} = (a, \mathbf{u})^\top = a + u_1 i + u_2 j + u_3 k
$$

and rotation described by a *rotation axis 𝐚* with unit length and an *angle 𝜃* can be represented by a quaternion:

$$
\mathbf{q} =
\left(
\cos\frac{\theta}{2},
\mathbf{a}\cdot\sin\frac{\theta}{2}
\right)
$$

**Task:** Hence, to determine the quaternion, the rotation axis and rotation angle need to be calculated.

Only the rotation axis is invariant under a rotation.

Thus, to determine the rotation axis, we need to calculate the eigenvectors.

$$
\begin{aligned}
R \cdot \mathbf{x} &= I \cdot \mathbf{x} \\
R \cdot \mathbf{x} - I \cdot \mathbf{x} &= \mathbf{0} \\
(R - I) \cdot \mathbf{x} &= \mathbf{0} \\
(R - \lambda \cdot I) \cdot \mathbf{x} &= \mathbf{0}
\end{aligned}
$$

Hence

$$
\begin{aligned}
\left(
\begin{pmatrix}
0.36 & 0.48 & -0.8 \\
-0.8 & 0.6 & 0 \\
0.48 & 0.64 & 0.6
\end{pmatrix} -
\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{pmatrix}
\right)
\mathbf{x}
&= \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}
\\
\begin{pmatrix}
-0.64 & 0.48 & -0.8 \\
-0.8 & -0.4 & 0 \\
0.48 & 0.64 & -0.4
\end{pmatrix}
\begin{pmatrix}
x_1 \\ x_2 \\ x_3
\end{pmatrix}
&= \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}
\\
-0.64x_1 + 0.48x_2 - 0.8x_3 &= 0 \\
-0.8x_1 - 0.4x_2 &= 0 \\
0.48x_1 + 0.64x_2 - 0.4x_3 &= 0
\end{aligned}
$$

We need to solve this system of equation

Step 1: Eliminate $x_3$

$$
\begin{aligned}
(4)\quad 2(3)-(1): \qquad
&1.6x_1 + 0.8x_2 = 0
\\
(5)\quad 2(2)+(4): \qquad
&0=0
\end{aligned}
$$

This shows a linear dependency. Therefore, one variable can be chosen freely:

$$
x_1=c
$$

Step 2: Calculate $x_2$

Substitute $x_1=c$ into equation (2):

$$
\begin{aligned}
-0.8c-0.4x_2 &= 0 \\
x_2 &= -\frac{0.8}{0.4}c \\
&= -2c
\end{aligned}
$$

Step 3: Calculate $x_3$

Substitute $x_1=c$ and $x_2=-2c$ into equation (3):

$$
\begin{aligned}
0.48c+0.64(-2c)-0.4x_3 &= 0 \\
-0.8c-0.4x_3 &= 0 \\
x_3 &= -\frac{0.8}{0.4}c \\
&= -2c
\end{aligned}
$$

The rotation axis must have unit length:

$$
\|\mathbf{x}\|=1
$$

The eigenvector is:

$$
\mathbf{x}_c =
c
\begin{pmatrix}
1\\
-2\\
-2
\end{pmatrix}
$$

Step 1: Apply the normalization constraint

$$
\begin{aligned}
\|\mathbf{x}_c\| &= 1\\
\sqrt{c^2(1^2+(-2)^2+(-2)^2)} &= 1\\
\sqrt{9c^2} &= 1\\
3|c| &= 1
\end{aligned}
$$

Step 2: Solve for $c$

$$
c=\pm\frac{1}{3}
$$

Step 3: Calculate the normalized rotation axis

$$
\boxed{
\mathbf{a} =
\pm\frac{1}{3}
\begin{pmatrix}
1\\
-2\\
-2
\end{pmatrix}
}
$$

Both signs represent the same rotation axis with opposite orientation.

Next we need to find the **angle** by which we rotate. In genral there are two approaches:
1. Trace(𝑅): Sum of the elements on the diagonal, in this case: Trace(A) = 1.56 = 1 = 2 cos a => cos a = 0.28 => a - \pm 73.7
2. Rotation of an orthogonal vector


The rotated vector is given by:

$$
\mathbf{v}'=R\cdot\mathbf{v}
$$

The rotation angle between $\mathbf{v}$ and $\mathbf{v}'$ is:

$$
\cos(\alpha)=
\frac{\mathbf{v}\cdot\mathbf{v}'}
{\|\mathbf{v}\|\cdot\|\mathbf{v}'\|}
$$

1. Choose a vector perpendicular to the rotation axis

Given $\mathbf{v}\in\mathbb{R}^3$, with $\mathbf{v}\neq\mathbf{0}$ and $\mathbf{v}\cdot\mathbf{x}=0$, i.e. $\mathbf{v}\perp\mathbf{x}$:

$$
\mathbf{x}=\frac{1}{3}
\begin{pmatrix}
1\\-2\\-2
\end{pmatrix}
\qquad
\mathbf{v}=
\begin{pmatrix}
0\\1\\-1
\end{pmatrix}
$$

2. Calculate the rotated vector

$$
\begin{aligned}
\mathbf{v}' &= R\cdot\mathbf{v}
\\[6pt]
&=
\begin{pmatrix}
0.36 & 0.48 & -0.8\\
-0.8 & 0.6 & 0\\
0.48 & 0.64 & 0.6
\end{pmatrix}
\cdot
\begin{pmatrix}
0\\1\\-1
\end{pmatrix}
\\[8pt]
&=
\begin{pmatrix}
0.48+(-1)\cdot(-0.8)\\
0.6\\
0.64+(-1)\cdot0.6
\end{pmatrix}
\\[8pt]
&=
\begin{pmatrix}
1.28\\
0.6\\
0.04
\end{pmatrix}
\end{aligned}
$$

3. Calculate the rotation angle

$$
\begin{aligned}
\cos(\alpha)
&=
\frac{\mathbf{v}\cdot\mathbf{v}'}
{\|\mathbf{v}\|\cdot\|\mathbf{v}'\|}
\\[6pt]
&=
\frac{0.6+(-1)\cdot0.04}{\sqrt{2}\cdot\sqrt{2}}
\\[6pt]
&=\frac{0.56}{2}=0.28
\end{aligned}
$$

$$
\begin{aligned}
\alpha
&=\arccos(0.28)
\\
&\approx 1.287\text{ rad}
\\
&\approx 73.7^\circ
\end{aligned}
$$

4. Determine the sign of the rotation angle

Use the cross product and the rotation axis:

$$
\begin{aligned}
(\mathbf{v}\times\mathbf{v}')\cdot\mathbf{x}
&=
\|\mathbf{v}\|\cdot\|\mathbf{v}'\|\sin(\alpha)
\\
&=2\sin(\alpha)=1.92
\end{aligned}
$$

$$
\begin{aligned}
\sin(\alpha)&=0.96>0
\\
\Rightarrow\quad \alpha&=+1.287\text{ rad}
\end{aligned}
$$

Final result$$
\boxed{\alpha\approx +1.287\text{ rad}=+73.7^\circ}
$$

{{< /details >}}



### Exercise 3 (Small Exercises)

a) Which rotation does the following quaternion describe? 𝐪 = 0, 0,1,0

b) Do the quaternions corresponding to the following angle-axis rotations differ?
- $0^\circ$ rotation around $(0,0,1)$
- $0^\circ$ rotation around $\left(0,\frac{1}{2},\frac{1}{2}\right)$

c) What is the unit quaternion corresponding to a rotation by 60° around (0,4,3) ⊤?

{{< details "Solution a)" "false" >}}

**Solution**: 180° around y-axis

**Explanation:**
$$
\mathbf{q} =
\left(
\cos\frac{\alpha}{2},
\mathbf{x}\cdot\sin\frac{\alpha}{2}
\right)
$$

Scalar-first notation (as used in the lecture); scalar-last notation also exists.

Here:

$$
\mathbf{x}=
\begin{pmatrix}
0\\1\\0
\end{pmatrix}
\qquad \text{(y-axis)}
$$

$$
\begin{aligned}
\cos\frac{\alpha}{2}&=0\\
\frac{\alpha}{2}&=90^\circ\\
\alpha&=180^\circ
\end{aligned}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

**Solution:** No 
**Explanation:** 
$$
\mathbf{q}=
\left(
\cos\frac{\alpha}{2},
\mathbf{x}\cdot\sin\frac{\alpha}{2}
\right)
$$

In both cases: $\alpha=0$, thus

$$
\cos\frac{\alpha}{2}=1
\qquad\text{and}\qquad
\sin\frac{\alpha}{2}=0
$$

For any $\mathbf{x}$:

$$
\mathbf{x}\cdot 0=\mathbf{0}
$$

Therefore:

$$
\boxed{
\mathbf{q}_1=\mathbf{q}_2=(1,0,0,0)
}
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

$$
\mathbf{q}=
\left(
\cos\frac{\alpha}{2},
\mathbf{x}\cdot\sin\frac{\alpha}{2}
\right)
$$

Calculate the sine and cosine:

$$
\begin{aligned}
\cos\frac{\alpha}{2}
&=\cos 30^\circ=\frac{\sqrt{3}}{2}
\\
\sin\frac{\alpha}{2}
&=\sin 30^\circ=\frac{1}{2}
\end{aligned}
$$

Normalize the rotation axis:

$$
\begin{aligned}
\mathbf{x}
&=
\frac{1}{\sqrt{0^2+4^2+3^2}}
\begin{pmatrix}
0\\4\\3
\end{pmatrix}
\\
&=
\frac{1}{5}
\begin{pmatrix}
0\\4\\3
\end{pmatrix}
\\
&=
\begin{pmatrix}
0\\0.8\\0.6
\end{pmatrix}
\end{aligned}
$$

Calculate the quaternion:

$$
\begin{aligned}
\mathbf{q}
&=
\left(
\frac{\sqrt{3}}{2},
\begin{pmatrix}
0\\0.8\\0.6
\end{pmatrix}
\cdot\frac12
\right)
\\[6pt]
&=
\boxed{
\left(
\frac{\sqrt{3}}{2},
0,0.4,0.3
\right)
}
\end{aligned}
$$

{{< /details >}}



### Exercise 4 (Homogeneous Matrices)

Let $T\in SE(3)$ be a homogeneous transformation matrix and $\mathbf{p}=(1,2,3)^\top$ be a position vector, with

$$
T=
\begin{pmatrix}
0 & 0 & 1 & 5\\
0 & 1 & 0 & 0\\
-1 & 0 & 0 & 0\\
0 & 0 & 0 & 1
\end{pmatrix}
$$

a) Describe the transformation represented by $T$.

b) Apply the transformation described by $T$ to $\mathbf{p}$.

c) Determine the inverse transformation matrix $T^{-1}$.


{{< details "Solution a)" "false" >}}

Rotation by $90^\circ$ around the y-axis:

$$
R_y(\alpha)=
\begin{pmatrix}
\cos\alpha & 0 & \sin\alpha\\
0 & 1 & 0\\
-\sin\alpha & 0 & \cos\alpha
\end{pmatrix}
$$

$$
\begin{aligned}
R_y(90^\circ)
&=
\begin{pmatrix}
\cos90^\circ & 0 & \sin90^\circ\\
0 & 1 & 0\\
-\sin90^\circ & 0 & \cos90^\circ
\end{pmatrix}
\\[8pt]
&=
\boxed{
\begin{pmatrix}
0 & 0 & 1\\
0 & 1 & 0\\
-1 & 0 & 0
\end{pmatrix}
}
\end{aligned}
$$


Translation by 5 along the x-axis:

$$
t =
\begin{pmatrix}
5\\
0\\
0
\end{pmatrix}
$$
{{< /details >}}


{{< details "Solution b)" "false" >}}

$$
\begin{aligned}
\mathbf{p}' &=
\begin{pmatrix}
0 & 0 & 1 & 5\\
0 & 1 & 0 & 0\\
-1 & 0 & 0 & 0\\
0 & 0 & 0 & 1
\end{pmatrix}
\cdot
\begin{pmatrix}
1\\2\\3\\1
\end{pmatrix}
\\[10pt]
&=
\begin{pmatrix}
1\cdot3+5\cdot1\\
1\cdot2\\
-1\cdot1\\
1\cdot1
\end{pmatrix}
\\[10pt]
&=
\begin{pmatrix}
8\\2\\-1\\1
\end{pmatrix}
\end{aligned}
$$

The transformed position (without the homogeneous coordinate) is:

$$
\boxed{
\mathbf{p}'=
\begin{pmatrix}
8\\2\\-1
\end{pmatrix}
}
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

General formula for the inverse transformation

$$
T\cdot T^{-1}=I_4
$$

$$
\begin{pmatrix}
R & \mathbf{t}\\
\mathbf{0}^{\top} & 1
\end{pmatrix}
\cdot
\begin{pmatrix}
A & \mathbf{b}\\
\mathbf{0}^{\top} & 1
\end{pmatrix} =
\begin{pmatrix}
I_3 & \mathbf{0}\\
\mathbf{0}^{\top} & 1
\end{pmatrix}
$$

From matrix multiplication:

$$
\begin{aligned}
R\cdot A+\mathbf{t}\cdot\mathbf{0}^{\top}
&=I_3
\\
R\cdot A&=I_3
\\
A&=R^{-1}=R^\top
\end{aligned}
$$

For the translation component:

$$
\begin{aligned}
R\cdot\mathbf{b}+\mathbf{t}\cdot1&=\mathbf{0}
\\
R\cdot\mathbf{b}&=-\mathbf{t}
\\
\mathbf{b}&=-R^\top\cdot\mathbf{t}
\end{aligned}
$$

Therefore, the general inverse transformation is:

$$
\boxed{
T^{-1}=
\begin{pmatrix}
R^\top & -R^\top\cdot\mathbf{t}\\
\mathbf{0}^{\top} & 1
\end{pmatrix}
}
$$

Determine $T^{-1}$ for the given transformation

Given:

$$
T=
\begin{pmatrix}
0 & 0 & 1 & 5\\
0 & 1 & 0 & 0\\
-1 & 0 & 0 & 0\\
0 & 0 & 0 & 1
\end{pmatrix}
$$

Extract the rotation matrix and translation vector:

$$
R=
\begin{pmatrix}
0 & 0 & 1\\
0 & 1 & 0\\
-1 & 0 & 0
\end{pmatrix}
\qquad
\mathbf{t}=
\begin{pmatrix}
5\\0\\0
\end{pmatrix}
$$

1. Calculate the transposed rotation matrix

$$
R^\top=
\begin{pmatrix}
0 & 0 & -1\\
0 & 1 & 0\\
1 & 0 & 0
\end{pmatrix}
$$

2. Calculate the inverse translation vector

$$
\begin{aligned}
-R^\top\cdot\mathbf{t}
&= -
\begin{pmatrix}
0 & 0 & -1\\
0 & 1 & 0\\
1 & 0 & 0
\end{pmatrix}
\cdot
\begin{pmatrix}
5\\0\\0
\end{pmatrix}
\\[8pt]
&= -
\begin{pmatrix}
0\\0\\5
\end{pmatrix}
\\[8pt]
&=
\begin{pmatrix}
0\\0\\-5
\end{pmatrix}
\end{aligned}
$$

3. Assemble the inverse transformation matrix

$$
\boxed{
T^{-1}=
\begin{pmatrix}
0 & 0 & -1 & 0\\
0 & 1 & 0 & 0\\
1 & 0 & 0 & -5\\
0 & 0 & 0 & 1
\end{pmatrix}
}
$$

{{< /details >}}



### Exercise 5 (Concatenation of Coordinate Transformations)

Consider a service robot with a holonomic platform. The robot's $x$-axis points forward, and the $z$-axis points upward. The $y$-axis is chosen such that the coordinate system is right-handed.

The initial pose of the robot in the base coordinate system (BCS) is given by:

$$
T_{\text{init}} =
\begin{bmatrix}
1 & 0 & 0 & 5\\
0 & 1 & 0 & 3\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$

The following commands are sent to the robot and executed in sequence:

1. Rotate about the $z$-axis by $90^\circ$.
2. Drive straight ahead by $4$ units.
3. Drive straight ahead by $2$ units and $3$ units to the right, and finally rotate about the $z$-axis by $-45^\circ$.

Calculate the transformation matrices for the individual commands as well as the final pose of the robot in the BCS.


{{< details "Solution" "false" >}}

1. First Transformation: Rotation by $90^\circ$

The robot rotates around its local $z$-axis by $90^\circ$.

$$
{}^{init}T_1 =
\begin{bmatrix}
0 & -1 & 0 & 0\\
1 & 0 & 0 & 0\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$

2. Second Transformation: Drive Forward by 4 Units

The robot moves 4 units forward along its local $x$-axis.

$$
{}^1T_2 =
\begin{bmatrix}
1 & 0 & 0 & 4\\
0 & 1 & 0 & 0\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$

3. Third Transformation: Translation and Rotation

The robot performs the following movements:
- Moves 2 units forward along its local $x$-axis.
- Moves 3 units to the right along its local negative $y$-axis.
- Rotates around its local $z$-axis by $-45^\circ$.

The rotation matrix is:

$$
R_z(-45^\circ)=
\begin{bmatrix}
\cos(-45^\circ) & -\sin(-45^\circ) & 0\\
\sin(-45^\circ) & \cos(-45^\circ) & 0\\
0 & 0 & 1
\end{bmatrix}
$$

we obtain:

$$
{}^2T_3 =
\begin{bmatrix}
\frac{\sqrt{1}}{2} & \frac{\sqrt{1}}{2} & 0 & 2\\
-\frac{\sqrt{1}}{2} & \frac{\sqrt{1}}{2} & 0 & -3\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$

4. Final Transformation

The final transformation is calculated by multiplying the initial pose with all three local transformations:

$$
T_{\text{final}} =
T_{\text{init}}
\cdot {}^{init}T_1
\cdot {}^1T_2
\cdot {}^2T_3
$$

Therefore:

$$
\boxed{
T_{\text{final}}=
\begin{bmatrix}
\frac{\sqrt{1}}{2} & -\frac{\sqrt{1}}{2} & 0 & 8\\
\frac{\sqrt{1}}{2} & \frac{\sqrt{1}}{2} & 0 & 9\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
}
$$

5. Final Robot Pose


$$
\boxed{
\mathbf{p}_{\text{final}}=
\begin{bmatrix}
8\\9\\0
\end{bmatrix}
}
$$

{{< /details >}}



### Exercise 6 (Distance Between Poses)

The current pose $T_{\text{TCP}}$ and the target pose $T_{\text{Goal}}$ of an end effector are given as:

Current pose:

$$
T_{\text{TCP}}=
\begin{bmatrix}
0&-1&0&1\\
1&0&0&2\\
0&0&1&3\\
0&0&0&1
\end{bmatrix}
$$

Target pose:

$$
T_{\text{Goal}}=
\begin{bmatrix}
0&0&-1&7\\
0&1&0&6\\
1&0&0&5\\
0&0&0&1
\end{bmatrix}
$$


Calculate the translational distance, The linear distance between the current position of the end effector and its target position, and the Rotational distance, The angular difference between the current orientation and the target orientation.


{{< details "Solution" "false" >}}

**Translational Distance**

$$
\Delta\mathbf{t}=
\begin{bmatrix}7\\6\\5\end{bmatrix} -
\begin{bmatrix}1\\2\\3\end{bmatrix} =
\begin{bmatrix}6\\4\\2\end{bmatrix}
$$

Euclidean distance:

$$
\Delta t=\sqrt{6^2+4^2+2^2}
=\sqrt{56} \approx
\boxed{7.48}
$$

**Rotational Distance**

We want the rotation from the current orientation to the target orientation:

$$
R_{TCP}\cdot R_{Goal} = R_{\text{Goal}}
$$

Hence

$$
R_{\text{Goal}}^{\text{TCP}}=R_{TCP}^{-1}\cdot R_{Goal}
$$

Since rotation matrices are orthogonal:

$$
R_{TCP}^{-1}=R_{TCP}^{T}
$$

Therefore:

$$
R_{\text{Goal}}^{\text{TCP}}=
\begin{bmatrix}
0&1&0\\
-1&0&0\\
0&0&1
\end{bmatrix}
\begin{bmatrix}
0&0&-1\\
0&1&0\\
1&0&0
\end{bmatrix} =
\begin{bmatrix}
0&1&0\\
0&0&1\\
1&0&0
\end{bmatrix}
$$


For a 3D rotation matrix, the trace (sum of diagonal elements) is related to the rotation angle by:

$$
\operatorname{Trace}(R)=1+2\cos(\Delta\alpha)
$$

Thus

$$
\operatorname{Trace}(R_{\text{Goal}}^{\text{TCP}})=0+0+0=0
$$

Substituting:

$$
0=1+2\cos(\Delta\alpha)
$$

$$
\cos(\Delta\alpha)=-0.5
$$

$$
\Delta\alpha=\arccos(-0.5)
$$

Final Result

$$
\boxed{\Delta\alpha=120^\circ\approx2.094\text{ rad}}
$$

{{< /details >}}




### Exercise 7 (Quaternions)

Consider the point

$$
\mathbf p=\begin{bmatrix}5\\1\\7\end{bmatrix}
$$

the rotation axis

$$
\mathbf a=\begin{bmatrix}0\\0\\1\end{bmatrix}
$$

and the rotation angle

$$
\phi=90^\circ.
$$

a) Represent the point $\mathbf p$ as a quaternion $\mathbf v$.

b) Determine the rotation quaternion $\mathbf q$ and its conjugate $\mathbf q^*$.

c) Rotate the point using quaternion multiplication and determine $\mathbf p'$.

d) Derive the SLERP interpolation between two given quaternions and calculate it for $t=\frac12$.


{{< details "Solution a)" "false" >}}

A 3D point is represented as a quaternion with a zero scalar part

$$
\mathbf v=0+5i+1j+7k
$$

Therefore:

$$
\boxed{\mathbf v=(0,5,1,7)}
$$

{{< /details >}}


{{< details "Solution b)" "false" >}}

$$
\mathbf q=
\left(\cos\frac{\phi}{2},\mathbf a\sin\frac{\phi}{2}\right)
$$

Substituting $\phi=90^\circ$ and $\mathbf a=(0,0,1)$:

$$
\mathbf q=(\cos45^\circ,0,0,\sin45^\circ)
$$

$$
\boxed{\mathbf q=\left(\frac{\sqrt2}{2},0,0,\frac{\sqrt2}{2}\right)}
$$

The conjugate reverses the signs of the imaginary components:

$$
\boxed{\mathbf q^*=\left(\frac{\sqrt2}{2},0,0,-\frac{\sqrt2}{2}\right)}
$$

{{< /details >}}


{{< details "Solution c)" "false" >}}

The rotated point is calculated using:

$$
\mathbf v'=\mathbf q\cdot\mathbf v\cdot\mathbf q^*
$$

Substituting:

$$
=\frac12(1+k)(5i+j+7k)\frac12(1-k)
$$

First multiplication:

$$
=\frac12(-7+4i+6j+7k)\frac12(1-k)
$$

Second multiplication:

$$
=\frac12(0-2i+10j+14k)
$$

Simplifying:

$$
\mathbf v'=0-i+5j+7k
$$

Therefore:

$$
\boxed{\mathbf v'=(0,-1,5,7)}
$$

The resulting rotated point is:

$$
\boxed{\mathbf p'=(-1,5,7)}
$$

{{< /details >}}


{{< details "Solution d)" "false" >}}

Given:

$$
\mathbf q_1=(0,1,0,0)=i
$$

$$
\mathbf q_2=(0,0,1,0)=j
$$

$$
t=0.5
$$

The SLERP formula is:

$$
\operatorname{SLERP}(\mathbf q_1,\mathbf q_2,t) =
\frac{\sin((1-t)\theta)}{\sin\theta}\mathbf q_1
+
\frac{\sin(t\theta)}{\sin\theta}\mathbf q_2
$$

For these quaternions, $\theta=\frac{\pi}{2}$.

Substituting $t=0.5$:

$$
=\frac{\sin(\pi/4)}{\sin(\pi/2)}\mathbf q_1
+
\frac{\sin(\pi/4)}{\sin(\pi/2)}\mathbf q_2
$$

$$
=\frac{\sqrt2}{2}\mathbf q_1+
\frac{\sqrt2}{2}\mathbf q_2
$$

Therefore:

$$
=\frac{\sqrt2}{2}i+\frac{\sqrt2}{2}j
$$

Final result$$
\boxed{
\mathbf q(0.5)=
\left(0,\frac{\sqrt2}{2},\frac{\sqrt2}{2},0\right)
}
$$

{{< /details >}}
