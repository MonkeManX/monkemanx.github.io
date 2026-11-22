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

Calculate the quaternion \(q\) that describes the rotation given by \(R_2\).

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

Step 1: Eliminate \(x_3\)

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

Step 2: Calculate \(x_2\)

Substitute \(x_1=c\) into equation (2):

$$
\begin{aligned}
-0.8c-0.4x_2 &= 0 \\
x_2 &= -\frac{0.8}{0.4}c \\
&= -2c
\end{aligned}
$$

Step 3: Calculate \(x_3\)

Substitute \(x_1=c\) and \(x_2=-2c\) into equation (3):

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

Step 2: Solve for \(c\)

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

The rotation angle between \(\mathbf{v}\) and \(\mathbf{v}'\) is:

$$
\cos(\alpha)=
\frac{\mathbf{v}\cdot\mathbf{v}'}
{\|\mathbf{v}\|\cdot\|\mathbf{v}'\|}
$$

1. Choose a vector perpendicular to the rotation axis

Given \(\mathbf{v}\in\mathbb{R}^3\), with \(\mathbf{v}\neq\mathbf{0}\) and \(\mathbf{v}\cdot\mathbf{x}=0\), i.e. \(\mathbf{v}\perp\mathbf{x}\):

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
- \(0^\circ\) rotation around \((0,0,1)\)
- \(0^\circ\) rotation around \(\left(0,\frac{1}{2},\frac{1}{2}\right)\)

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

In both cases: \(\alpha=0\), thus

$$
\cos\frac{\alpha}{2}=1
\qquad\text{and}\qquad
\sin\frac{\alpha}{2}=0
$$

For any \(\mathbf{x}\):

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

Let \(T\in SE(3)\) be a homogeneous transformation matrix and \(\mathbf{p}=(1,2,3)^\top\) be a position vector, with

$$
T=
\begin{pmatrix}
0 & 0 & 1 & 5\\
0 & 1 & 0 & 0\\
-1 & 0 & 0 & 0\\
0 & 0 & 0 & 1
\end{pmatrix}
$$

a) Describe the transformation represented by \(T\).

b) Apply the transformation described by \(T\) to \(\mathbf{p}\).

c) Determine the inverse transformation matrix \(T^{-1}\).


{{< details "Solution a)" "false" >}}

Rotation by \(90^\circ\) around the y-axis:

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

Determine \(T^{-1}\) for the given transformation

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

Consider a service robot with a holonomic platform. The robot's \(x\)-axis points forward, and the \(z\)-axis points upward. The \(y\)-axis is chosen such that the coordinate system is right-handed.

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

1. Rotate about the \(z\)-axis by \(90^\circ\).
2. Drive straight ahead by \(4\) units.
3. Drive straight ahead by \(2\) units and \(3\) units to the right, and finally rotate about the \(z\)-axis by \(-45^\circ\).

Calculate the transformation matrices for the individual commands as well as the final pose of the robot in the BCS.


{{< details "Solution" "false" >}}

1. First Transformation: Rotation by \(90^\circ\)

The robot rotates around its local \(z\)-axis by \(90^\circ\).

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

The robot moves 4 units forward along its local \(x\)-axis.

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
- Moves 2 units forward along its local \(x\)-axis.
- Moves 3 units to the right along its local negative \(y\)-axis.
- Rotates around its local \(z\)-axis by \(-45^\circ\).

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

The current pose \(T_{\text{TCP}}\) and the target pose \(T_{\text{Goal}}\) of an end effector are given as:

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

a) Represent the point \(\mathbf p\) as a quaternion \(\mathbf v\).

b) Determine the rotation quaternion \(\mathbf q\) and its conjugate \(\mathbf q^*\).

c) Rotate the point using quaternion multiplication and determine \(\mathbf p'\).

d) Derive the SLERP interpolation between two given quaternions and calculate it for \(t=\frac12\).


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

Substituting \(\phi=90^\circ\) and \(\mathbf a=(0,0,1)\):

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

For these quaternions, \(\theta=\frac{\pi}{2}\).

Substituting \(t=0.5\):

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


### Exercise 8 (Transformations)

In this task, the root pose of a robot and its relation to the base coordinate system (BCS) is considered. In a second step, the relation to a target pose is included.

#### 8.1. Interpretation of a Pose

Let the initial root pose of the robot, described in the BCS, be given as

$$
{}^{BCS}T_{root}=
\begin{bmatrix}
\frac{1}{2}\sqrt{3} & -\frac{1}{2} & 0 & 3 \\
\frac{1}{2} & \frac{1}{2}\sqrt{3} & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

a) Which transformation does \({}^{BCS}T_{root}\) describe?

b) At which position is the robot’s root located? Draw the position in the BCS.

To describe the orientation of the robot, we use the orthonormal basis vectors of the local coordinate system tied to the robot’s root. We define the x-axis as pointing into the direction of motion, the y-axis to point left, and the z-axis to point upwards.

c) Write down the end points of the orthonormal basis vectors \({}^{root}v_{x}\), \({}^{root}v_{y}\) and \({}^{root}v_{z}\) and the vector of the origin \({}^{root}v_{o}\).

d) Calculate the representation of these vectors in BCS. Use the result to draw the robot’s root coordinate system in the BCS.


{{< details "Solution a)" "false" >}}

A homogeneous transformation matrix consists of two parts:

\\[ T = \begin{pmatrix} R & \mathbf{t}\\\ \mathbf{0}^T & 1 \end{pmatrix} \\]

The transformation consists of:

- Translation: 3 units along the global x-axis.
- Rotation around the z-axis of the BCS by 30°

{{< /details >}}

{{< details "Solution b)" "false" >}}

{{< img src="/attachments/robotics/robotics_excerise_8_1_ii.png" width="70%" >}}

{{< /details >}}


{{< details "Solution c)" "false" >}}

- Its origin is at \((0,0,0)\).
- Its forward direction (x-axis) is \((1,0,0)\).
- Its left direction (y-axis) is \((0,1,0)\).
- Its upward direction (z-axis) is \((0,0,1)\).

{{< /details >}}

{{< details "Solution d)" "false" >}}

To clauclate teh rperesnetation in BCS we ned to apply the trnfoamrtion matrix to our vecotrs in lcoal presnetation, because them atrix is homogenous i.e has also a translation component we need to add a 1 to them 

$$
{}^{BCS}\mathbf{v}_i = {}^{BCS}T_{root} \begin{pmatrix} \mathbf{v}_i\\1 \end{pmatrix}
$$

So this means

$$
{}^{BCS}\mathbf{v}_x =  \begin{pmatrix} 3+\frac{\sqrt{3}}{2}\\ \frac{1}{2}\\ 0\\ 1 \end{pmatrix}
$$

$$
{}^{BCS}\mathbf{v}_y = \begin{pmatrix} 3-\frac{1}{2}\\ \frac{\sqrt{3}}{2}\\ 0\\ 1 \end{pmatrix}
$$

$$
{}^{BCS}\mathbf{v}_z = \begin{pmatrix} 3\\ 0\\ 1\\ 1 \end{pmatrix}
$$

$$
{}^{BCS}\mathbf{v}_o = \begin{pmatrix} 3\\ 0\\ 0\\ 1 \end{pmatrix}
$$

{{< img src="/attachments/robotics/robotics_excerise_8_1_iv.png" width="70%" >}}

{{< /details >}}


#### 8.2. Conversion Between Coordinate Systems

A target pose \({}^{BCS}T_{root}\) is given as

$$
{}^{BCS}T_{root}=
\begin{bmatrix}
0 & -1 & 0 & 3+\sqrt{3} \\
1 & 0 & 0 & 1 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

a) Draw the target pose in the BCS.

b) Calculate the pose of the target in the robot’s root coordinate system.

c) Calculate the pose of the robot root in the target coordinate system.


{{< details "Solution a)" "false" >}}

{{< img src="/attachments/robotics/robotics_excerise_8_2_i.png" width="70%" >}}

{{< /details >}}

{{< details "Solution b)" "false" >}}

The target pose is given in the base coordinate system (BCS). To express the target pose in the robot's root coordinate system, the transformation between the BCS and the root coordinate system must be inverted and multiplied by the target transformation.

The known relation is:

\\[ {}^{\text{BCS}}T\_{\text{root}} \cdot {}^{\text{root}}T\_{\text{target}} = {}^{\text{BCS}}T\_{\text{target}} \\]

Rearranging yields:

\\[ {}^{\text{root}}T\_{\text{target}} = ({}^{\text{BCS}}T\_{\text{root}})^{-1} \cdot {}^{\text{BCS}}T\_{\text{target}} \\]

First, the inverse transformation is calculated:

\\[ {}^{\text{BCS}}T\_{\text{root}}^{-1} = \begin{bmatrix} \frac{1}{2} & \frac{3}{2} & -\frac{1}{2} & 3\\\ -\frac{1}{2} & \frac{1}{2} & 0 & 0\\\ 0 & 0 & 1 & 0\\\ 0 & 0 & 0 & 1 \end{bmatrix} \\]

Substituting the matrices into the equation gives:

\\[ {}^{\text{root}}T\_{\text{target}} = \begin{bmatrix} \frac{1}{2} & \frac{3}{2} & -\frac{1}{2} & 3\\\ -\frac{1}{2} & \frac{1}{2} & 0 & 0\\\ 0 & 0 & 1 & 0\\\ 0 & 0 & 0 & 1 \end{bmatrix} \cdot \begin{bmatrix} 0 & -1 & 0 & 3\\\ 1 & 0 & 0 & 1\\\ 0 & 0 & 1 & 0\\\ 0 & 0 & 0 & 1 \end{bmatrix} \\]

Performing the matrix multiplication results in:

\\[ \boxed{ {}^{\text{root}}T\_{\text{target}} = \begin{bmatrix} \frac{1}{2} & -\frac{1}{2} & \frac{3}{2} & 3\\\ \frac{1}{2} & \frac{3}{2} & 0 & 0\\\ 0 & 0 & 1 & 0\\\ 0 & 0 & 0 & 1 \end{bmatrix} } \\]

This matrix describes the target pose relative to the robot's root coordinate system.

{{< /details >}}

{{< details "Solution c)" "false" >}}

See b)

{{< /details >}}


#### 8.3. Local and Global Transformation

Whether a transformation is applied from the left or from the right is important.

a) Write down a transformation \(T\) that corresponds to a \(60^\circ\) rotation around the z-axis.

b) Apply \(T\) to \({}^{BCS}T_{root}\) from the left. Draw the resulting coordinate system \({}^{BCS}T_{trans, L}\).

c) Apply \(T\) to \({}^{BCS}T_{root}\) from the right. Draw the resulting coordinate system \({}^{BCS}T_{trans, R}\).

d) Which of both transformations corresponds to a rotation around local axes, and which one around global axes?


{{< details "Solution a)" "false" >}}

The homogeneous transformation matrix for a rotation of \\(60^\circ\\) around the z-axis is given by:

\\[ T = \begin{bmatrix} \cos(60^\circ) & -\sin(60^\circ) & 0 & 0\\\ \sin(60^\circ) & \cos(60^\circ) & 0 & 0\\\ 0 & 0 & 1 & 0\\\ 0 & 0 & 0 & 1 \end{bmatrix} \\]

Using

\\[ \cos(60^\circ)=\frac{1}{2}, \qquad \sin(60^\circ)=\frac{\sqrt{3}}{2} \\]

the resulting transformation matrix is:

\\[ \boxed{ T = \begin{bmatrix} \frac{1}{2} & -\frac{\sqrt{3}}{2} & 0 & 0\\\ \frac{\sqrt{3}}{2} & \frac{1}{2} & 0 & 0\\\ 0 & 0 & 1 & 0\\\ 0 & 0 & 0 & 1 \end{bmatrix} } \\]
 
{{< /details >}}

{{< details "Solution b-d)" "false" >}}

{{< img src="/attachments/robotics/robotics_excerise_8_3.png" width="70%" >}}

{{< /details >}}

### Exercise 9 (Denavit Hartenberg)

#### Task 9.1 

Transform the given right-handed coordinate frames into new coordinate frames using the provided Denavit-Hartenberg (DH) parameters.

Sketch the solution, including all auxiliary coordinate frames and the parameters that lead to the final result.

{{< img src="/attachments/robotics/robotics_excerise_9_1.png" width="100%" >}}


{{< details "Solution a)" "false" >}}

{{< img src="/attachments/robotics/robotics_excerise_9_1_a_1.png" width="80%" >}}
{{< img src="/attachments/robotics/robotics_excerise_9_1_a_2.png" width="80%" >}}
{{< img src="/attachments/robotics/robotics_excerise_9_1_a_3.png" width="80%" >}}
{{< img src="/attachments/robotics/robotics_excerise_9_1_a_4.png" width="80%" >}}

{{< /details >}}


{{< details "Solution b)" "false" >}}

{{< img src="/attachments/robotics/robotics_excerise_9_1_b_1.png" width="80%" >}}
{{< img src="/attachments/robotics/robotics_excerise_9_1_b_2.png" width="80%" >}}
{{< img src="/attachments/robotics/robotics_excerise_9_1_b_3.png" width="80%" >}}
{{< img src="/attachments/robotics/robotics_excerise_9_1_b_4.png" width="80%" >}}

{{< /details >}}


#### Task 9.2 

The following schematic representation of a robot arm is given. The base coordinate
system (BCS, frame 0) is defined by (x0, y0, z0). For a joint angle of θ2 = 0, the robot
arm is horizontal. Determine the DH parameters of joints 1–3, using the BCS, and fill
in the following table:


{{< img src="/attachments/robotics/robotics_excerise_9_2.png" width="80%" >}}

{{< details "Solution a)" "false" >}}

{{< img src="/attachments/robotics/robotics_excerise_9_2_1.png" width="80%" >}}

{{< img src="/attachments/robotics/robotics_excerise_9_2_2.png" width="80%" >}}

{{< /details >}}


### Exercise 10 (Jacobian Matrix)


Consider the following crane with one revolute joint at its base and two prismatic joints along the crane boom.


{{< img src="/attachments/robotics/robotics_excerise_10.png" width="60%" >}}

The base coordinate system (BCS, frame 0) is located at the foot of the tower. The \\(z_0\\)-axis points upwards, and for \\(\theta_1 = 0\\), the crane boom points in the direction of the \\(x_0\\)-axis.

The homogeneous transformation of the end-effector pose relative to the BCS is given by:

\\[ {}^0T_3 = \begin{pmatrix} \cos(\theta_1+90^\circ) & \sin(\theta_1+90^\circ) & 0 & \sin(\theta_1+90^\circ)d_2\\\ \sin(\theta_1+90^\circ) & -\cos(\theta_1+90^\circ) & 0 & -\cos(\theta_1+90^\circ)d_2\\\ 0 & 0 & -1 & -d_3+20\\\ 0 & 0 & 0 & 1 \end{pmatrix} \\]

a). Determine the Jacobian matrix of the end-effector. Describe its orientation using roll-pitch-yaw angles \\((\alpha,\beta,\gamma)\\), as introduced in the lecture.


b) The following configurations \\(q_A\\) and \\(q_B\\), as well as the joint velocities, are given. The distances \\(d_2\\) and \\(d_3\\) are given in meters. Joint velocities are given in rad/s for joint 1 and m/s for joints 2 and 3.

*Joint configurations:*

\\[ q_A = \begin{pmatrix} 90^\circ\\\ 10\\\ 10 \end{pmatrix} \qquad q_B = \begin{pmatrix} 180^\circ\\\ 3\\\ 15 \end{pmatrix} \\]

*Joint velocities:*

\\[ \dot q_1 = \begin{pmatrix} 1\\\ 1\\\ 1 \end{pmatrix} \qquad \dot q_2 = \begin{pmatrix} -1\\\ -1\\\ 0 \end{pmatrix} \qquad \dot q_3 = \begin{pmatrix} 2\\\ -1\\\ 2 \end{pmatrix} \\]

*i.)* \\(q_A,\ \dot q_1\\)

*ii.)* \\(q_A,\ \dot q_2\\)

*iii.)* \\(q_B,\ \dot q_2\\)

*iv.)* \\(q_B,\ \dot q_3\\)

{{< details "Solution a)" "false" >}}


The Jacobian matrix describes the relationship between the joint velocities and the end-effector velocities. Each column corresponds to one joint variable.

The joint configuration is defined as

\\[ q = \begin{pmatrix} \theta_1\\\ d_2\\\ d_3 \end{pmatrix} \\]

The Jacobian is defined as

\\[ J = \frac{\partial f}{\partial q} = \begin{pmatrix} \frac{\partial f}{\partial \theta_1} & \frac{\partial f}{\partial d_2} & \frac{\partial f}{\partial d_3} \end{pmatrix} \in \mathbb{R}^{6\times 3} \\]

where the end-effector pose is described by

\\[ f(\theta_1,d_2,d_3) = \begin{pmatrix} x\\\y\\\z\\\\\alpha\\\\\beta\\\\\gamma \end{pmatrix} \\]

### **1. Determine the end-effector position**

The homogeneous transformation is given as

\\[ {}^0T_3 = \begin{pmatrix} \cos(\theta_1+90^\circ) & \sin(\theta_1+90^\circ) & 0 & \sin(\theta_1+90^\circ)d_2\\\ \sin(\theta_1+90^\circ) & -\cos(\theta_1+90^\circ) & 0 & -\cos(\theta_1+90^\circ)d_2\\\ 0 & 0 & -1 & -d_3+20\\\ 0 & 0 & 0 & 1 \end{pmatrix} \\]

Extracting the position coordinates gives

\\[ \begin{aligned} x &= \sin(\theta_1+90^\circ)d_2\\\ y &= -\cos(\theta_1+90^\circ)d_2\\\ z &= -d_3+20 \end{aligned} \\]

### **2. Determine the end-effector orientation (RPY)**

The rotation matrix is described using the roll-pitch-yaw convention:

\\[ R = R_z(\gamma)R_y(\beta)R_x(\alpha) \\]

The corresponding rotation matrix is

\\[ R = \begin{pmatrix} c\_\beta c\_\gamma & s\_\alpha s\_\beta c\_\gamma-c\_\alpha s\_\gamma & s\_\alpha s\_\gamma+c\_\alpha s\_\beta c\_\gamma\\\ c\_\beta s\_\gamma & s\_\alpha s\_\beta s\_\gamma+c\_\alpha c\_\gamma & c\_\alpha s\_\beta s\_\gamma-s\_\alpha c\_\gamma\\\ -s\_\beta & s\_\alpha c\_\beta & c\_\alpha c\_\beta \end{pmatrix} \\]

where \\(c_x=\cos(x)\\) and \\(s_x=\sin(x)\\).

Comparing this with the rotation part of the given transformation matrix:

\\[ R = \begin{pmatrix} \cos(\theta_1+90^\circ) & \sin(\theta_1+90^\circ) & 0\\\ \sin(\theta_1+90^\circ) & -\cos(\theta_1+90^\circ) & 0\\\ 0 & 0 & -1 \end{pmatrix} \\]

we can determine the individual angles.

**Determine&#x20;**\\(\beta\\)**:**

Using the element in the third row and first column:

\\[ -\sin(\beta)=0 \\]

\\[ \boxed{\beta=0} \\]

**Determine&#x20;**\\(\alpha\\)**:**

Using the elements in the third row:

\\[ \sin(\alpha)\cos(\beta)=0 \\]

\\[ \cos(\alpha)\cos(\beta)=-1 \\]

Since \\(\beta=0\\), this gives

\\[ \sin(\alpha)=0,\qquad \cos(\alpha)=-1 \\]

Therefore,

\\[ \boxed{\alpha=\pi} \\]

**Determine&#x20;**\\(\gamma\\)**:**

Using the elements in the first column:

\\[ \cos(\beta)\cos(\gamma)=\cos(\theta_1+90^\circ) \\]

\\[ \cos(\beta)\sin(\gamma)=\sin(\theta_1+90^\circ) \\]

Since \\(\beta=0\\):

\\[ \boxed{\gamma=\theta_1+90^\circ} \\]

Thus, the complete end-effector pose is described by

\\[ f(\theta_1,d_2,d_3)= \begin{pmatrix} \sin(\theta_1+90^\circ)d_2\\\ -\cos(\theta_1+90^\circ)d_2\\\ -d_3+20\\\ \pi\\\ 0\\\ \theta_1+90^\circ \end{pmatrix} \\]

### **3. Calculate the Jacobian matrix**

The Jacobian consists of the partial derivatives of the end-effector pose with respect to each joint variable.

**Column 1: Partial derivatives with respect to&#x20;**\\(\theta_1\\)

\\[ \frac{\partial f}{\partial \theta_1} = \begin{pmatrix} \frac{\partial x}{\partial \theta_1}\\\ \frac{\partial y}{\partial \theta_1}\\\ \frac{\partial z}{\partial \theta_1}\\\ \frac{\partial \alpha}{\partial \theta_1}\\\ \frac{\partial \beta}{\partial \theta_1}\\\ \frac{\partial \gamma}{\partial \theta_1} \end{pmatrix} \\]

Evaluating the derivatives:

\\[ \begin{aligned} \frac{\partial x}{\partial \theta_1} &=\cos(\theta_1+90^\circ)d_2\\\ \frac{\partial y}{\partial \theta_1} &=\sin(\theta_1+90^\circ)d_2\\\ \frac{\partial z}{\partial \theta_1} &=0\\\ \frac{\partial \alpha}{\partial \theta_1} &=0\\\ \frac{\partial \beta}{\partial \theta_1} &=0\\\ \frac{\partial \gamma}{\partial \theta_1} &=1 \end{aligned} \\]

Therefore,

\\[ \boxed{ \frac{\partial f}{\partial \theta_1} = \begin{pmatrix} \cos(\theta_1+90^\circ)d_2\\\ \sin(\theta_1+90^\circ)d_2\\\ 0\\\ 0\\\ 0\\\ 1 \end{pmatrix} } \\]

**Column 2: Partial derivatives with respect to&#x20;**\\(d_2\\)

\\[ \frac{\partial f}{\partial d_2} = \begin{pmatrix} \frac{\partial x}{\partial d_2}\\\ \frac{\partial y}{\partial d_2}\\\ \frac{\partial z}{\partial d_2}\\\ \frac{\partial \alpha}{\partial d_2}\\\ \frac{\partial \beta}{\partial d_2}\\\ \frac{\partial \gamma}{\partial d_2} \end{pmatrix} \\]

Evaluating the derivatives:

\\[ \begin{aligned} \frac{\partial x}{\partial d_2} &=\sin(\theta_1+90^\circ)\\\ \frac{\partial y}{\partial d_2} &=-\cos(\theta_1+90^\circ)\\\ \frac{\partial z}{\partial d_2} &=0\\\ \frac{\partial \alpha}{\partial d_2} &=0\\\ \frac{\partial \beta}{\partial d_2} &=0\\\ \frac{\partial \gamma}{\partial d_2} &=0 \end{aligned} \\]

Therefore,

\\[ \boxed{ \frac{\partial f}{\partial d_2} = \begin{pmatrix} \sin(\theta_1+90^\circ)\\\ -\cos(\theta_1+90^\circ)\\\ 0\\\ 0\\\ 0\\\ 0 \end{pmatrix} } \\]

**Column 3: Partial derivatives with respect to&#x20;**\\(d_3\\)

\\[ \frac{\partial f}{\partial d_3} = \begin{pmatrix} \frac{\partial x}{\partial d_3}\\\ \frac{\partial y}{\partial d_3}\\\ \frac{\partial z}{\partial d_3}\\\ \frac{\partial \alpha}{\partial d_3}\\\ \frac{\partial \beta}{\partial d_3}\\\ \frac{\partial \gamma}{\partial d_3} \end{pmatrix} \\]

Evaluating the derivatives:

\\[ \begin{aligned} \frac{\partial x}{\partial d_3}&=0\\\ \frac{\partial y}{\partial d_3}&=0\\\ \frac{\partial z}{\partial d_3}&=-1\\\ \frac{\partial \alpha}{\partial d_3}&=0\\\ \frac{\partial \beta}{\partial d_3}&=0\\\ \frac{\partial \gamma}{\partial d_3}&=0 \end{aligned} \\]

Therefore,

\\[ \boxed{ \frac{\partial f}{\partial d_3} = \begin{pmatrix} 0\\\ 0\\\ -1\\\ 0\\\ 0\\\ 0 \end{pmatrix} } \\]

### **4. Assemble the Jacobian matrix**

Combining all three columns gives the final Jacobian matrix:

\\[ \boxed{ J = \begin{pmatrix} \cos(\theta_1+90^\circ)d_2 & \sin(\theta_1+90^\circ) & 0\\\ \sin(\theta_1+90^\circ)d_2 & -\cos(\theta_1+90^\circ) & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} } \\]

This is the \\(6\times3\\) Jacobian matrix mapping the joint velocities to the end-effector linear velocities and RPY angle rates:

\\[ \dot f = J\dot q \\]

Note: For differentiation, \\(\theta_1\\) is measured in radians, so that \\(\partial\gamma/\partial\theta_1=1\\). The given \\(90^\circ\\) is equivalent to \\(\pi/2\\).

{{< /details >}}

{{< details "Solution b)" "false" >}}


The end-effector velocity is calculated by multiplying the Jacobian matrix with the corresponding joint velocity vector:

\\[ \dot{\mathbf{x}} = J(\mathbf{q}) \cdot \dot{\mathbf{q}} \\]

The resulting velocity vector contains the linear velocities and the RPY angular rates:

\\[ \dot{\mathbf{x}} = \begin{pmatrix} \dot{x}\\\ \dot{y}\\\ \dot{z}\\\ \dot{\alpha}\\\ \dot{\beta}\\\ \dot{\gamma} \end{pmatrix} \\]

### **i.) Configuration&#x20;**\\(q_A\\)**&#x20;and joint velocity&#x20;**\\(\dot{q}\_1\\)

Given:

\\[ q_A = \begin{pmatrix} 90^\circ\\\10\\\10 \end{pmatrix}, \qquad \dot{q}\_1 = \begin{pmatrix} 1\\\1\\\1 \end{pmatrix} \\]

First, evaluate the Jacobian at \\(q_A\\):

\\[ \theta_1+90^\circ=180^\circ \\]

\\[ \cos(180^\circ)=-1, \qquad \sin(180^\circ)=0 \\]

Substituting these values into the Jacobian gives:

\\[ J(q_A)= \begin{pmatrix} -10 & 0 & 0\\\ 0 & 1 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \\]

Multiplying by the joint velocity vector:

\\[ \dot{\mathbf{x}} = \begin{pmatrix} -10 & 0 & 0\\\ 0 & 1 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \begin{pmatrix} 1\\\1\\\1 \end{pmatrix} \\]

The resulting end-effector velocity is:

\\[ \boxed{ \dot{\mathbf{x}}= \begin{pmatrix} -10\\\ 1\\\ -1\\\ 0\\\ 0\\\ 1 \end{pmatrix} } \\]

### **ii.) Configuration&#x20;**\\(q_A\\)**&#x20;and joint velocity&#x20;**\\(\dot{q}\_2\\)

Given:

\\[ q_A = \begin{pmatrix} 90^\circ\\\10\\\10 \end{pmatrix}, \qquad \dot{q}\_2 = \begin{pmatrix} -1\\\\-1\\\0 \end{pmatrix} \\]

The Jacobian for \\(q_A\\) has already been calculated:

\\[ J(q_A)= \begin{pmatrix} -10 & 0 & 0\\\ 0 & 1 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \\]

Multiplying by the joint velocity vector:

\\[ \dot{\mathbf{x}} = \begin{pmatrix} -10 & 0 & 0\\\ 0 & 1 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \begin{pmatrix} -1\\\\-1\\\0 \end{pmatrix} \\]

The resulting end-effector velocity is:

\\[ \boxed{ \dot{\mathbf{x}}= \begin{pmatrix} 10\\\ -1\\\ 0\\\ 0\\\ 0\\\ -1 \end{pmatrix} } \\]

### **iii.) Configuration&#x20;**\\(q_B\\)**&#x20;and joint velocity&#x20;**\\(\dot{q}\_2\\)

Given:

\\[ q_B = \begin{pmatrix} 180^\circ\\\3\\\15 \end{pmatrix}, \qquad \dot{q}\_2 = \begin{pmatrix} -1\\\\-1\\\0 \end{pmatrix} \\]

First, evaluate the Jacobian at \\(q_B\\):

\\[ \theta_1+90^\circ=270^\circ \\]

\\[ \cos(270^\circ)=0, \qquad \sin(270^\circ)=-1 \\]

Substituting these values into the Jacobian gives:

\\[ J(q_B)= \begin{pmatrix} 0 & -1 & 0\\\ -3 & 0 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \\]

Multiplying by the joint velocity vector:

\\[ \dot{\mathbf{x}} = \begin{pmatrix} 0 & -1 & 0\\\ -3 & 0 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \begin{pmatrix} -1\\\\-1\\\0 \end{pmatrix} \\]

The resulting end-effector velocity is:

\\[ \boxed{ \dot{\mathbf{x}}= \begin{pmatrix} 1\\\ 3\\\ 0\\\ 0\\\ 0\\\ -1 \end{pmatrix} } \\]

### **iv.) Configuration&#x20;**\\(q_B\\)**&#x20;and joint velocity&#x20;**\\(\dot{q}\_3\\)

Given:

\\[ q_B = \begin{pmatrix} 180^\circ\\\3\\\15 \end{pmatrix}, \qquad \dot{q}\_3 = \begin{pmatrix} 2\\\\-1\\\2 \end{pmatrix} \\]

The Jacobian for \\(q_B\\) has already been calculated:

\\[ J(q_B)= \begin{pmatrix} 0 & -1 & 0\\\ -3 & 0 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \\]

Multiplying by the joint velocity vector:

\\[ \dot{\mathbf{x}} = \begin{pmatrix} 0 & -1 & 0\\\ -3 & 0 & 0\\\ 0 & 0 & -1\\\ 0 & 0 & 0\\\ 0 & 0 & 0\\\ 1 & 0 & 0 \end{pmatrix} \begin{pmatrix} 2\\\\-1\\\2 \end{pmatrix} \\]

The resulting end-effector velocity is:

\\[ \boxed{ \dot{\mathbf{x}}= \begin{pmatrix} 1\\\ -6\\\ -2\\\ 0\\\ 0\\\ 2 \end{pmatrix} } \\]

{{< /details >}}


## Exercise 11 (Inverse Kinematics)

Given is a SCARA robot with one prismatic joint \\(d_1\\) and two revolute joints \\(\theta_2\\) and \\(\theta_3\\).

The forward kinematics are defined as:

\\[ f(q)= \begin{pmatrix} -500\sin(\theta_2)\cos(\theta_3) -500\cos(\theta_2)\sin(\theta_3) -500\sin(\theta_2) \\\ 500\cos(\theta_2)\cos(\theta_3) -500\sin(\theta_2)\sin(\theta_3) +100+500\cos(\theta_2) \\\ d_1 \end{pmatrix} \\]

All lengths are given in mm, all angles in radians, and all velocities in mm/s (translation) or rad/s (rotation).

The robot configuration is:

\\[ q= \begin{pmatrix} d_1\\\ \theta_2\\\ \theta_3 \end{pmatrix} \\]

The joint velocity, based on the inverse Jacobian, is given by:

\\[ \dot{q}=J^{-1}(q)\dot{x} \\]

*a). Determine the Inverse Jacobian*

Determine the inverse Jacobian matrix \\(J^{-1}(q)\\) for the given SCARA robot. The orientation of the end-effector can be ignored.

**b). Determine the Joint Velocities*

Determine the joint velocity \\(\dot{q}\\) that results in the following end-effector velocity:

\\[ \dot{x}= \begin{pmatrix} 1000\\\ 0\\\ 0 \end{pmatrix} \\]

The robot configuration is:

\\[ q= \begin{pmatrix} 1\\\ 0\\\ \frac{\pi}{2} \end{pmatrix} \\]

*c). Determine the Singularities*

In which robot configurations do singularities occur? Identify the corresponding joint configurations and explain the conditions under which the inverse Jacobian becomes undefined.


{{< details "Solution a)" "false" >}}

The forward kinematics of the SCARA robot are

\\[ \mathbf{f}(\mathbf{q})= \begin{pmatrix} -500\sin(\theta_2+\theta_3)-500\sin(\theta_2)\\\ 500\cos(\theta_2+\theta_3)+100+500\cos(\theta_2)\\\ d_1 \end{pmatrix}, \\]

with the joint configuration

\\[ \mathbf{q}= \begin{pmatrix} d_1\\\ \theta_2\\\ \theta_3 \end{pmatrix}. \\]

The relationship between Cartesian and joint velocities is

\\[ \dot{\mathbf{x}}=J(\mathbf{q})\dot{\mathbf{q}}. \\]

Therefore, the inverse Jacobian is required to calculate the joint velocities from Cartesian velocities:

\\[ \dot{\mathbf{q}}=J^{-1}(\mathbf{q})\dot{\mathbf{x}}. \\]

### **1. Calculate the Jacobian**

The Jacobian is obtained by differentiating the forward kinematics with respect to the joint variables:

\\[ J(\mathbf{q})= \frac{\partial\mathbf{f}}{\partial\mathbf{q}}. \\]

The partial derivatives are

\\[ \begin{aligned} \frac{\partial x}{\partial d_1}&=0, & \frac{\partial x}{\partial\theta_2} &=-500\cos(\theta_2+\theta_3)-500\cos(\theta_2), & \frac{\partial x}{\partial\theta_3} &=-500\cos(\theta_2+\theta_3), \\\\[2mm] \frac{\partial y}{\partial d_1}&=0, & \frac{\partial y}{\partial\theta_2} &=-500\sin(\theta_2+\theta_3)-500\sin(\theta_2), & \frac{\partial y}{\partial\theta_3} &=-500\sin(\theta_2+\theta_3), \\\\[2mm] \frac{\partial z}{\partial d_1}&=1, & \frac{\partial z}{\partial\theta_2}&=0, & \frac{\partial z}{\partial\theta_3}&=0. \end{aligned} \\]

Thus, the Jacobian matrix is

\\[ \boxed{ J(\mathbf{q})= \begin{pmatrix} 0 & -500\cos(\theta_2+\theta_3)-500\cos(\theta_2) & -500\cos(\theta_2+\theta_3) \\\ 0 & -500\sin(\theta_2+\theta_3)-500\sin(\theta_2) & -500\sin(\theta_2+\theta_3) \\\ 1&0&0 \end{pmatrix}. } \\]

### **2. Calculate the determinant**

To calculate the inverse, we first determine the determinant of the Jacobian.

Expanding along the first column gives

\\[ \begin{aligned} \det J(\mathbf{q}) ={}&250000 \left(\cos(\theta_2+\theta_3)+\cos(\theta_2)\right) \sin(\theta_2+\theta_3) \\\ &-250000\cos(\theta_2+\theta_3) \left(\sin(\theta_2+\theta_3)+\sin(\theta_2)\right). \end{aligned} \\]

After expanding and cancelling the common terms:

\\[ \begin{aligned} \det J(\mathbf{q}) =250000\big[& \cos(\theta_2)\sin(\theta_2+\theta_3) \\\ &-\cos(\theta_2+\theta_3)\sin(\theta_2) \big]. \end{aligned} \\]

Using the trigonometric identity

\\[ \sin(a-b)=\sin(a)\cos(b)-\cos(a)\sin(b), \\]

we obtain

\\[ \begin{aligned} \det J(\mathbf{q}) &=250000\sin((\theta_2+\theta_3)-\theta_2)\\\ &=250000\sin(\theta_3). \end{aligned} \\]

Therefore,

\\[ \boxed{\det J(\mathbf{q})=500^2\sin(\theta_3).} \\]

### **3. Calculate the inverse Jacobian**

The inverse of a square matrix is calculated using its adjugate and determinant:

\\[ J^{-1}(\mathbf{q}) = \frac{1}{\det J(\mathbf{q})} \operatorname{adj}(J(\mathbf{q})). \\]

Since the first column of the Jacobian is \\((0,0,1)^T\\), its inverse can be calculated by inverting the upper-left \\(2\times2\\) block.

Let

\\[ B= \begin{pmatrix} -500\cos(\theta_2+\theta_3)-500\cos(\theta_2) & -500\cos(\theta_2+\theta_3) \\\ -500\sin(\theta_2+\theta_3)-500\sin(\theta_2) & -500\sin(\theta_2+\theta_3) \end{pmatrix}. \\]

For a \\(2\times2\\) matrix

\\[ B= \begin{pmatrix} a&b\\\ c&d \end{pmatrix}, \\]

the inverse is

\\[ B^{-1} = \frac{1}{ad-bc} \begin{pmatrix} d&-b\\\ -c&a \end{pmatrix}. \\]

Applying this formula gives

\\[ \begin{aligned} B^{-1} =\frac{1}{250000\sin(\theta_3)} \begin{pmatrix} -500\sin(\theta_2+\theta_3) & 500\cos(\theta_2+\theta_3) \\\ 500\sin(\theta_2+\theta_3)+500\sin(\theta_2) & -500\cos(\theta_2+\theta_3)-500\cos(\theta_2) \end{pmatrix}. \end{aligned} \\]

Including the prismatic joint \\(d_1\\), the complete inverse Jacobian is

\\[ \boxed{ J^{-1}(\mathbf{q})= \begin{pmatrix} 0&0&1\\\\[2mm] -\dfrac{\sin(\theta_2+\theta_3)}{500\sin(\theta_3)} & \dfrac{\cos(\theta_2+\theta_3)}{500\sin(\theta_3)} &0\\\\[4mm] \dfrac{\sin(\theta_2+\theta_3)+\sin(\theta_2)} {500\sin(\theta_3)} & -\dfrac{\cos(\theta_2+\theta_3)+\cos(\theta_2)} {500\sin(\theta_3)} &0 \end{pmatrix}. } \\]

This is the required inverse Jacobian. It maps Cartesian velocities to joint velocities according to

\\[ \boxed{ \dot{\mathbf{q}}=J^{-1}(\mathbf{q})\dot{\mathbf{x}}. } \\]

{{< /details >}}


{{< details "Solution b)" "false" >}}

We are given the Cartesian velocity

\\[ \dot{\mathbf{x}}= \begin{pmatrix} 1000\\\ 0\\\ 0 \end{pmatrix} \\]

and the joint configuration

\\[ \mathbf{q}= \begin{pmatrix} d_1\\\ \theta_2\\\ \theta_3 \end{pmatrix} = \begin{pmatrix} 1\\\ 0\\\ \frac{\pi}{2} \end{pmatrix}. \\]

The goal is to determine the corresponding joint velocities \\(\dot{\mathbf{q}}\\).

### **1. Inverse Jacobian**

From Exercise 4.1, the inverse Jacobian is

\\[ J^{-1}(\mathbf{q})= \begin{pmatrix} 0&0&1\\\\[2mm] -\dfrac{\sin(\theta_2+\theta_3)}{500\sin(\theta_3)} & \dfrac{\cos(\theta_2+\theta_3)}{500\sin(\theta_3)} &0\\\\[4mm] \dfrac{\sin(\theta_2+\theta_3)+\sin(\theta_2)} {500\sin(\theta_3)} & -\dfrac{\cos(\theta_2+\theta_3)+\cos(\theta_2)} {500\sin(\theta_3)} &0 \end{pmatrix}. \\]

The joint velocities are calculated using

\\[ \dot{\mathbf{q}}=J^{-1}(\mathbf{q})\dot{\mathbf{x}}. \\]

### **2. Evaluate the inverse Jacobian**

Substitute the given joint configuration:

\\[ \theta_2=0, \qquad \theta_3=\frac{\pi}{2}. \\]

The required trigonometric values are

\\[ \begin{aligned} \sin(\theta_2+\theta_3) &=\sin\left(\frac{\pi}{2}\right)=1,\\\ \cos(\theta_2+\theta_3) &=\cos\left(\frac{\pi}{2}\right)=0,\\\ \sin(\theta_2)&=\sin(0)=0,\\\ \cos(\theta_2)&=\cos(0)=1,\\\ \sin(\theta_3)&=\sin\left(\frac{\pi}{2}\right)=1. \end{aligned} \\]

Substituting these values into the inverse Jacobian gives

\\[ \begin{aligned} J^{-1}(\mathbf{q}) &= \begin{pmatrix} 0&0&1\\\\[2mm] -\dfrac{1}{500}&0&0\\\\[3mm] \dfrac{1+0}{500}& -\dfrac{0+1}{500}&0 \end{pmatrix}\\\\[2mm] &= \boxed{ \begin{pmatrix} 0&0&1\\\ -\frac{1}{500}&0&0\\\ \frac{1}{500}&-\frac{1}{500}&0 \end{pmatrix}. } \end{aligned} \\]

### **3. Calculate the joint velocities**

Now multiply the inverse Jacobian by the given Cartesian velocity:

\\[ \begin{aligned} \dot{\mathbf{q}} &=J^{-1}(\mathbf{q})\dot{\mathbf{x}}\\\\[2mm] &= \begin{pmatrix} 0&0&1\\\ -\frac{1}{500}&0&0\\\ \frac{1}{500}&-\frac{1}{500}&0 \end{pmatrix} \begin{pmatrix} 1000\\\ 0\\\ 0 \end{pmatrix}\\\\[3mm] &= \begin{pmatrix} 0\cdot1000+0\cdot0+1\cdot0\\\ -\frac{1}{500}\cdot1000\\\ \frac{1}{500}\cdot1000-\frac{1}{500}\cdot0 \end{pmatrix}\\\\[3mm] &= \begin{pmatrix} 0\\\ -2\\\ 2 \end{pmatrix}. \end{aligned} \\]

Therefore, the resulting joint velocities are

\\[ \boxed{ \dot{\mathbf{q}}= \begin{pmatrix} \dot d_1\\\ \dot\theta_2\\\ \dot\theta_3 \end{pmatrix} = \begin{pmatrix} 0\ \mathrm{mm/s}\\\ -2\ \mathrm{rad/s}\\\ 2\ \mathrm{rad/s} \end{pmatrix}. } \\]

The prismatic joint remains stationary, while the two revolute joints rotate in opposite directions.

{{< /details >}}


{{< details "Solution c)" "false" >}}

A square matrix \\(A\in\mathbb{R}^{n\times n}\\) has full rank if and only if its determinant is non-zero:

\\[ \boxed{ \operatorname{rank}(A)=n \iff \det(A)\neq 0. } \\]

For the SCARA robot, the Jacobian is

\\[ J(\mathbf{q})= \begin{pmatrix} 0 & -500\cos(\theta_2+\theta_3)-500\cos(\theta_2) & -500\cos(\theta_2+\theta_3)\\\ 0 & -500\sin(\theta_2+\theta_3)-500\sin(\theta_2) & -500\sin(\theta_2+\theta_3)\\\ 1 & 0 & 0 \end{pmatrix}. \\]

Its determinant is

\\[ \boxed{ \det J(\mathbf{q})=500^2\sin(\theta_3). } \\]

A singular configuration \\(\mathbf{q}\_{\mathrm{sing}}\\) occurs when the Jacobian is not of full rank. Therefore,

\\[ \det J(\mathbf{q}\_{\mathrm{sing}})=0. \\]

Substituting the determinant gives

\\[ \begin{aligned} 500^2\sin(\theta_3)&=0,\\\ \sin(\theta_3)&=0. \end{aligned} \\]

The sine function is zero for integer multiples of \\(\pi\\). Thus,

\\[ \boxed{ \theta_3=k\pi,\qquad k\in\mathbb{Z}. } \\]

Considering the joint range \\(0\leq\theta_3<2\pi\\), the possible singular configurations are

\\[ \theta_3=0 \qquad\text{or}\qquad \theta_3=\pi. \\]

Consequently, the singular configurations are

\\[ \boxed{ \mathbf{q}\_{\mathrm{sing},1}= \begin{pmatrix} d_1\\\ \theta_2\\\ 0 \end{pmatrix}, \qquad \mathbf{q}\_{\mathrm{sing},2}= \begin{pmatrix} d_1\\\ \theta_2\\\ \pi \end{pmatrix}. } \\]

Here, \\(d_1\\) and \\(\theta_2\\) can take arbitrary admissible values. The singularities occur when the two revolute links are aligned, either in the fully extended configuration (\\(\theta_3=0\\)) or in the fully folded configuration (\\(\theta_3=\pi\\)).

{{< /details >}}
