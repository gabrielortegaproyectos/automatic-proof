arXiv:2501.04781v1 [math.OC] 8 Jan 2025
# Inexact Catching-Up Algorithm for Moreau’s Sweeping Processes

# Juan Guillermo Garrido∗    †    ‡, Maximiliano Lioi and Emilio Vilches

# January 10, 2025

# Abstract

In this paper, we develop an inexact version of the catching-up algorithm for sweeping processes. We define a new notion of approximate projection, which is compatible with any numerical method for approximating exact projections, as this new notion is not restricted to remain strictly within the set. We provide several properties of the new approximate projections, which enable us to prove the convergence of the inexact catching-up algorithm in three general frameworks: prox-regular moving sets, subsmooth moving sets, and merely closed sets. Additionally, we apply our numerical results to address complementarity dynamical systems, particularly electrical circuits with ideal diodes. In this context, we implement the inexact catching-up algorithm using a primal-dual optimization method, which typically does not necessarily guarantee a feasible point. Our results are illustrated through an electrical circuit with ideal diodes. Our results recover classical existence results in the literature and provide new insights into the numerical simulation of sweeping processes.

# 1 Introduction

The sweeping process, originally introduced by J.-J. Moreau in a series of foundational papers [22, 23], was motivated by various concrete applications, including quasi-static evolution in plasticity, contact dynamics, and friction dynamics [24, 25]. Since then, it has garnered significant interest in the study of dynamical systems with time-dependent constraints, particularly in fields such as nonsmooth mechanics, crowd motion [9, 21], and, more recently, the modeling of electrical circuits [1]. A well-established existence theory for the sweeping process is now widely recognized (see, e.g., [8, 27]). Of particular interest is the case of prox-regular moving sets, where existence and uniqueness of solutions can be established using the so-called catching-up algorithm (see [8]). Originally introduced by J.-J. Moreau in [23] for convex sets, the catching-up algorithm consists of an implicit discretization of the sweeping process, resulting in an iteration based on the projection onto the moving set.

The numerical applicability of the catching-up algorithm relies on the ability to compute an exact projection formula for the moving sets. However, for most sets, obtaining an exact projection onto a closed set is not feasible, and only numerical approximations can be obtained. In this paper, we develop a theoretical framework for numerically approximating solutions to the sweeping process. Building on the work done in [11], we define a new notion of approximate projection that is compatible with any numerical method for approximating exact projections, as this new notion is not restricted to remain strictly within the set.

In this work, we provide several properties of approximate projections and propose a general numerical method for the sweeping process based on these approximate projections.

∗Departamento de Ingenier´ıa Matem´atica, Universidad de Chile, Santiago, Chile. E-mail: jgarrido@dim.uchile.cl

†Departamento de Ingenier´ıa Matem´atica, Universidad de Chile, Santiago, Chile. E-mail: mlioi@dim.uchile.cl

‡Instituto de Ciencias de la Ingenier´ıa, Universidad de O’Higgins, Rancagua, Chile. E-mail: emilio.vilches@uoh.cl

1

---

can be considered as an inexact version of the catching-up algorithm, for which we prove the convergence in three general cases: (i) prox-regular moving sets (without compactness assumptions), (ii) ball-compact subsmooth moving sets, and (iii) general ball-compact fixed closed set. As a result, our findings cover a wide range of existence for the sweeping process.

Additionally, we apply our numerical results to address complementarity dynamical systems, particularly electrical circuits with ideal diodes. In this context, we implement the inexact catching-up algorithm using a primal-dual optimization method, which typically does not guarantee a feasible point.

It is worth emphasizing that our results generalize the catching-up algorithm and provide significant insights into the numerical solution of sweeping processes.

The paper is organized as follows. Section 2 introduces the mathematical tools required for the presentation and develops the theoretical properties of approximate projections. Section 3 focuses on the proposed algorithm and its main properties. In Section 4, we prove the convergence of the algorithm when the moving set has uniformly prox-regular values, without assuming compactness. Section 5 addresses the convergence of the proposed algorithm for ball-compact subsmooth moving sets. Section 6 extends this analysis to the case of a fixed ball-compact set. Finally, Section 7 explores numerical techniques for tackling complementarity dynamical systems. In particular, we reformulate a specific class of these systems as a perturbed sweeping process, enabling the use of approximate projections. The paper ends with some concluding remarks.

# 2 Mathematical Preliminaries

From now on, H denotes a real Hilbert space, whose norm, denoted by ∥ · ∥, is induced by the inner product ⟨·, ·⟩. The closed (resp. open) ball centered at x with radius r > 0 is denoted by B[x, r] (resp. B(x, r)), and the closed unit ball is denoted by B. For a given set S ⊂ H, the support and the distance function of S at x ∈ H are defined, respectively, as

σ(x, S) = sup⟨x, z⟩ and dS(x) := inf ∥x − z∥.

A set S ⊂ H is called ball compact if the set S ∩ rB is compact for all r > 0. Given ρ ∈]0, +∞] and γ ∈]0, 1[, the ρ−enlargement and the γρ−enlargement of S are defined, respectively, as

Uρ(S) = {x ∈ H : dS(x) &#x3C; ρ} and Uγ (S) = {x ∈ H : dS(x) &#x3C; γρ}.

The Hausdorff distance between two sets A, B ⊂ H is defined as

Haus(A, B) := max{sup dB(x), sup dA(x)}.

A vector h ∈ H belongs to the Clarke tangent cone T(S; x) (see [12]); when for every sequence (xn) in S converging to x and every sequence of positive numbers (tn) converging to 0, there exists a sequence (hn) in H converging to h such that xn + tnhn ∈ S for all n ∈ N. This cone is closed and convex, and its negative polar N(S; x) is the Clarke normal cone to S at x ∈ S, that is,

N(S; x) := {v ∈ H : ⟨v, h⟩ ≤ 0 for all h ∈ T(S; x)}.

As usual, N(S; x) = ∅ if x ∈ / S. Through that normal cone, the Clarke subdifferential of a function f : H → R ∪ {+∞} is defined as

∂f(x) := {v ∈ H : (v, −1) ∈ N (epi f, (x, f(x)))},

where epi f := {(y, r) ∈ H × R : f(y) ≤ r} is the epigraph of f. When the function f is finite and locally Lipschitzian around x, the Clarke subdifferential is characterized (see, e.g., [13]) in the following simple and amenable way

∂f(x) = {v ∈ H : ⟨v, h⟩ ≤ f◦(x; h) for all h ∈ H}.

---

where

f◦(x; h) := lim sup
(t,y)→(0+,x)
t-1[f(y + th) − f(y)],

is the generalized directional derivative of the locally Lipschitzian function f at x in the direction h ∈ H. The function f◦(x; ·) is in fact the support of ∂f(x), i.e., f◦(x; h) = σ∂f(x). That characterization easily yields that the Clarke subdifferential of any locally Lipschitzian function is a set-valued map with nonempty and convex values satisfying the important property of upper semicontinuity from H into Hw. Let f : H → R ∪ {+∞} be an lsc (lower semicontinuous) function and x ∈ dom f. We say that

1. An element ζ ∈ H belongs to the proximal subdifferential of f at x, denoted by ∂Pf(x), if there exist two non-negative numbers σ and η such that

f(y) ≥ f(x) + ⟨ζ, y − x⟩ − σ∥y − x∥2 for all y ∈ B(x; η).

An element ζ ∈ H belongs to the Fréchet subdifferential of f at x, denoted by ∂Ff(x), if

lim inf f(x + h) − f(x) − ⟨ζ, h⟩ ≥ 0.
h→0 ∥h∥

An element ζ ∈ H belongs to the limiting subdifferential of f at x, denoted by ∂Lf(x), if there exist sequences (ζn) and (xn) such that ζn ∈ ∂Pf (xn) for all n ∈ N and xn → x, ζn ⇀ ζ, and f (xn) → f(x).

Through these concepts, we can define the proximal, Fréchet, and limiting normal cone of a given set S ⊂ H at x ∈ S, respectively, as

NP(S; x) := ∂PIS(x), NF(C; x) := ∂FIC(x) and NL(S; x) := ∂LIS(x),

where I (x) = 0 if x ∈ S and I (x) = +∞ if x ∈ S / S. It is well known that the normal cone and the distance function are related by the following formulas (see, e.g., [7, Theorem 4.1] and [13]):

NP(S; x) ∩ B = ∂PdS(x) and N(S; x) = co∗NL(S; x) = cl∗ (R+∂dS(x)) for all x ∈ S.

In this paper, we consider the prominent class of prox-regular sets. Introduced by Federer in [16] and later developed by Rockafellar, Poliquin, and Thibault in [29]. The prox-regularity generalizes and unifies convexity and nonconvex bodies with C2 boundary. We refer to [14, 30] for a survey.

# Definition 2.1.

Let S be a closed subset of H and ρ ∈ ]0, +∞]. The set S is called ρ−uniformly prox-regular if for all x ∈ S and ζ ∈ NP(S; x) one has

⟨ζ, x′ − x⟩ ≤ ∥ζ∥ ∥x′ − x∥2 for all x′ ∈ S.

It is clear that convex sets are ρ-uniformly prox-regular for any ρ > 0. The following proposition provides a characterization of uniformly prox-regular sets (see, e.g., [14]).

# Proposition 2.2.

Let S ⊂ H closed and ρ ∈ ]0, +∞]. The following assertions are equivalent:

1. S is ρ-uniformly prox-regular.
2. For any γ ∈ ]0, 1[ the projection is well-defined on Uγ(S) and for all u1, u2 ∈ Uγ(S), one has

∥ projS(u1) − projS(u2)∥ ≤ (1 − γ)-1∥u1 − u2∥.

---

(c)  For all *xi ∈ S, vi ∈ NP(S; xi) ∩ B, with i = 1, 2*, one has

⟨*v1 − v2, x1 − x2⟩ ≥ − 1 ∥x1 − x2*∥2,

ρ

that is, the set-valued mapping NP(S; ·) ∩ B is 1/ρ−hypomonotone.

(d)  For all *γ ∈ ]0, 1[, for all x′, x ∈ Uγ(S) and for all v ∈ ∂PdS(x*), one has

⟨*v, x′ − x⟩ ≤ 2ρ(11  2 ∥x′ − x∥2 + dS(x′) − dS(x*))

− *γ*

Another prominent class of sets is that of subsmooth sets, which encompasses the concepts of convex and uniformly prox-regular sets (see [3] and [30, Chapter 8] for a survey).

# Definition 2.3.

Let S be a closed subset of H. We say that S is subsmooth at *x0 ∈ S, if for every ε > 0 there exists δ > 0* such that

(1)         ⟨*ξ2 − ξ1, x2 − x1⟩ ≥ −ε ∥x2 − x1*∥ ,

whenever *x1, x2 ∈ B [x0, δ]∩S and ξi ∈ N (S; xi)∩B for i ∈ {1, 2}. The set S is said subsmooth if it is subsmooth at each point of S. We further say that S is uniformly subsmooth, if for every ε > 0 there exists δ > 0, such that (1) holds for all x1, x2 ∈ S satisfying ∥x1 − x2∥ ≤ δ and all ξi ∈ N (S; xi) ∩ B for i ∈ {1, 2}*.

Let (S(t))t∈I be a family of closed sets of H indexed by a nonempty set I. The family is called equi-uniformly subsmooth, if for all *ε > 0, there exists δ > 0 such that for all t ∈ I, the inequality (1) holds for all x1, x2 ∈ S(t) satisfying ∥x1 − x2∥ ≤ δ and all ξi ∈ N(S(t); xi) ∩ B with i ∈ {1, 2}*.

Given an interval I, a set-valued map *F : I ⇒ H is called measurable if, for every open set U of H, the inverse image F−1(U) = {t ∈ I : F(t) ∩ U = ∅} is a Lebesgue measurable set. Whenever H is separable and F takes nonempty and closed values, this definition is equivalent to the L ⊗ B(H)-measurability of the graph gph F := {(t, x) ∈ I × H : x ∈ F(t)}* (see, e.g., [28, Theorem 6.2.20]).

A set-valued map *F : H ⇒ H is called upper semicontinuous from H into Hw if, for every weakly closed set C ⊂ H, the inverse image F−1(C) is a closed set of H. If F is upper semicontinuous, it is well-known (see [28, Proposition 6.1.15 (c)]) that the map x      σF(x)(ξ) is upper semicontinuous for all ξ ∈ H*. Moreover, when F takes convex and weakly compact values, these two properties are equivalent (see [28, Proposition 6.1.17]).

The projection onto *S ⊂ H at x ∈ H* is the (possibly empty) set defined as

ProjS(*x) := {z ∈ S : dS(x) = ∥x − z∥*.

Whenever the projection set is a singleton, we denote it simply as *projS(x). In most applications, the projection is difficult to calculate numerically, and one must resort to approximations of this object. The first of them, defined for ε > 0 and studied in [11], is the so-called set of ε*-approximate projections, given by

projε(*x) := {z ∈ S : ∥x − z∥2 &#x3C; dS(x) + ε*},

which is always nonempty and open. It is clear that an element of the above set can be obtained through an appropriate optimization numerical method. However, the above definition requires that every approximate projection lies entirely within the set S. Hence, only optimization algorithms that ensure this condition can be used to obtain an approximate projection.

It is known that for any *x ∈ H where ProjS(x) = ∅*, the following formula holds:

(2)      *x − z ∈ dS(x)∂PdS(z) for all z ∈ ProjS(x)*.

The next result, proved in [11, Lemma 1], provides an approximate version of the above formula without the nonemptiness assumption on the projection.

---

# 2.4

Let S ⊂ H be a nonempty and closed set, x ∈ H and ε > 0. For each z ∈ projε(x) there is v ∈ projε(x) such that ∥z − v∥ &#x3C; 2√ε and x − z ∈ (4√ε + dS(x))∂PdS(v) + 3√εB.

# 2.5

Now, we define the main object of this paper. Given a set S ⊂ H, x ∈ H, and ε, η > 0, the set of ε − η approximate projections is defined as

projε,η(x) := {z ∈ Sη : ∥x − z∥2 &#x3C; d2(x) + ε},

where Sη ⊂ H is any closed set such that S ⊂ Sη ⊂ S + ηB.

# 2.6

Let η > 0 and Sη ⊂ H be any closed set such that S ⊂ Sη ⊂ S + ηB. Then, dSη(x) ≤ dS(x) ≤ dSη(x) + η for all x ∈ H.

Proof. Fix x ∈ H and let η > 0. Since S ⊂ Sη ⊂ S + ηB, we obtain that dS+ηB(x) ≤ dSη(x) ≤ dS(x), which proves the first inequality. To prove the second inequality, we observe that any x ∈ S + ηB can be written as x = s + ηb for some s ∈ S and b ∈ B. Hence, dS(x) ≤ ∥x − s∥ ≤ η. Moreover, if x ∉ S + ηB, then, according to [6, Lemma 2.1], dS+ηB(x) = dS(x) − η, which implies the result.

# 2.7

Let ε, η > 0, and assume that S ⊂ Sη ⊂ S + ηB. Then,

projε(x) ⊂ projε,η(x) ⊂ projε+2η(dS(x)+√ε)+η²(x) + ηB for all x ∈ H.

Proof. Fix x ∈ H. The first assertion follows directly from the definition of the ε − η approximate projection. To prove the second inclusion, let z ∈ projε,η(x). Then ∥x − z∥2 &#x3C; d2(x) + ε. Since z ∈ Sη ⊂ S + ηB, there exists s ∈ S, b ∈ B such that z = s + ηb. We observe that ∥x − s∥2 &#x3C; d2(x) + ε + 2η(dS(x) + √ε) + η². Hence, s ∈ projε+2η(dS(x)+√ε)+η²(x), which implies that z ∈ projε+2η(dS(x)+√ε)+η²(x) + ηB.

# 2.8

Let S ⊂ H be a nonempty, closed set, x ∈ H, and ε, η > 0. Then, for each z ∈ projε,η(x), there exists v ∈ projε′(x) such that ∥z − v∥ &#x3C; 2√ε′ + η and x − z ∈ (4√ε′ + dS(x))∂PdS(v) + (3√ε′ + η)B, where ε′ := ε + 2η(dS(x) + √ε) + η².

Proof. Fix x ∈ H and ε, η > 0, let z ∈ projε,η(x). Then, by Proposition 2.7, there exist s ∈ projε′(x) and b ∈ B such that z = s + ηb with ε′ := ε + 2η(dS(x) + √ε) + η². Then, according to Lemma 2.4, there is v ∈ projε′(x) such that ∥s − v∥ &#x3C; 2√ε′ and x − s ∈ (4√ε′ + dS(x))∂PdS(v) + 3√ε′B.

Since z − s ∈ ηB, we observe that ∥z − v∥ ≤ ∥z − s∥ + ∥s − v∥ &#x3C; 2√ε′ + η. Then, because x − z = (x − s) + (s − z), we get that x − z ∈ (4√ε′ + dS(x))∂PdS(v) + 3√ε′B + ηB, which proves the desired result.

---

The following result provides two important properties of ε−η projections. Note that the second statement corresponds to a generalization of property (b) in Proposition 2.2.

# Proposition 2.9.

Let S ⊂ H be a ρ-uniformly prox-regular set. Then, one has:

1. Let xn → x ∈ Uρ(S). Then for any (zn) and any pair of sequences of positive numbers (εn) and (ηn) converging to 0 with zn ∈ projεn,ηn (xn) for all n ∈ N, we have that zn → projS(x).
2. Let γ ∈ ]0, 1[ and η ∈ ]0, ρ[. Assume that η ∈ ]0, η0[ and ε ∈ ]0, ε0], where η0 and ε0 are such that

γ + 4β0   1 + 1    + 3η0 + 4β0 + γ  (4β0 + 2η0) = 1,

where β0 := √ε0 + η0 + √2η0γρ. Then, for all zi ∈ projε,η(xi) and xi ∈ Uγ(S) for i ∈ {1, 2}, we have

(1 −    )∥z1 − z2∥2 ≤    √ε′ + η   ∥x1 − x2∥2 + M√ε′ + Nη + ⟨x1 − x2, z1 − z2⟩,

where  := α + 4√ε′(1 + 1 ) + 3η +          4√ε′+α  4√ε′ + 2η    , α := max{dS(x1), dS(x2)}, ε′ :=

ε + 2η(α + √ε)) + η2,  M :=         4     ε′+α  (16     ε′ + 16η + 4) + 24 ε′ + 20η + 11 and N :=

4√ε′+α (4η + 2) + 4η + 5.

# Proof.

(a): We observe that for all n ∈ N

∥zn∥ ≤ ∥zn − xn∥ + ∥xn∥ ≤ dS(xn) + √εn + ∥xn∥.

Hence, since εn → 0 and xn → x, we obtain (zn) is bounded. On the other hand, since x ∈ Uρ(S), the projection projS(x) is well-defined and

∥zn − projS(x)∥2 = ∥zn − xn∥2 − ∥xn − projS(x)∥2 + 2⟨x − projS(x), zn − projS(x)⟩ + 2⟨zn − projS(x), xn − x⟩

≤ d2 (xn) + εn − ∥xn − projS(x)∥2 + 2⟨x − projS(x), zn⟩ + 2⟨zn − projS(x), xn − x⟩

≤ εn + 2⟨x − projS(x), zn⟩ + 2⟨zn − projS(x)∥ · ∥xn − x∥,

where we have used that zn ∈ projεn,ηn (xn) and the fact that d2 (xn) ≤ ∥xn − projS(x)∥2. On the other hand, since zn ∈ S ⊂ S + Sηn, we observe that there exists sn ∈ S and bn ∈ B such that zn = sn + ηnbn.

Hence,

2⟨x − projS(x), zn − projS(x)⟩ = 2⟨x − projS(x), sn − projS(x)⟩ + 2⟨x − projS(x), ηnbn⟩.

Moreover, according to inclusion (2) and the ρ-uniform prox-regularity of S, we obtain that

2⟨x − projS(x), sn − projS(x)⟩ ≤ dS(x) ∥sn − projS(x)∥2

= dS(x) ∥zn − ηnbn − projS(x)∥2

≤ dS(x)       ∥zn − projS(x)∥2 + 2ηn∥zn − projS(x)∥ + η2,

where we have used that zn ∈ projεn,ηn (xn) and the fact that d2 (xn) ≤ ∥xn − projS(x)∥2.

---

where we have used that zn = sn + ηnbn. Therefore,

∥zn − projS(x)∥2 ≤ εn + dS(x) ∥zn − projS(x)∥2 + 2ηn∥zn − projS(x)∥ + η2

ρ

+ 2ηndS(x) + 2∥zn − projS(x)∥ · ∥xn − x∥.

Rearranging terms, we obtain that

∥zn − projS(x)∥2 ≤ ρεn + dS(x) 2ηn∥zn − projS(x)∥ + η2

ρ − dS(x) ρ − dS(x)

+ ρ − ρ (2ηndS(x) + 2∥zn − projS(x)∥ · ∥xn − x∥).

Finally, since xn → x, (zn) is bounded, εn → 0 and ηn → 0, we concluded that zn → projS(x).

(b): For i = 1, 2, let zi ∈ projε,η(xi). By virtue of Lemma 2.8, there exist vi, bi ∈ H for i ∈ {1, 2} such that

ε′ xi − zi − (3 ε′ + η)bi

bi ∈ B, vi ∈ proji(xi), ∥zi − vi∥ ≤ 2 ε′ + η and i ∈ ∂PdS(vi),

where ε′ := ε + 2η(dS(xi) + √ε) + η2. Hence, for i ∈ {1, 2}, one has

xi − zi − (3 ε′ + η)bi ∈ NP(S; vi) ∩ τB for all τ ≥ 4 ε′ + dS(xi).

For i ∈ {1, 2}, let us consider

xi − zi − (3 ε′ + η)bi

ζi := 4√ε′ + i ∈ NP(S; vi) ∩ B,

where α := max{dS(x1), dS(x2)} and ε′ = max{ε′1, ε′2} = ε + 2η(α + √ε) + η2. Since S is ρ−uniformly prox-regular and vi ∈ S, using the hypomonotonicity of the truncated proximal normal cone (see Proposition 2.2 (c)), we obtain that

(3) ⟨ζ1 − ζ2, v1 − v2⟩ ≥ − 1 ∥v1 − v2∥2.

On the one hand, since ∥zi − vi∥ ≤ 2 ε′ + η for i ∈ {1, 2}, we get that

(4) ∥v1 − v2∥ ≤ ∥v1 − z1∥ + ∥z1 − z2∥ + ∥z2 − v2∥ ≤ 4√ε′ + 2η + ∥z1 − z2∥,

and for all z ∈ H and i ∈ {1, 2}, one has

√ ′ η ∥z∥2 ∥zi − vi∥2 √ ′ η ∥z∥2 √ ′

(5) |⟨z, vi − zi⟩| ≤ (ε + 2) 2 + 2(√ε′ + η) ≤ (ε + 2) 2 + 2 ε + η.

Due to (4) we get that

⟨(x1 − z1 − (3 ε′ + η)b1) − (x2 − z2 − (3 ε′ + η)b2), v1 − v2⟩

= ⟨(3 ε′ + η)b2 − (3 ε′ + η)b1, v1 − v2⟩ + ⟨x1 − x2, v1 − v2⟩ − ⟨z1 − z2, v1 − v2⟩

≤ 24ε′ 2 √ ′ 2 1 √ ′

= 24ε′ + 20√ε′η + 4η2 + (6√ε′ + 2η)∥z1 − z2∥ + ⟨x1 − x2, v1 − v2⟩ − ⟨z1 − z2, v1 − z1⟩

≤ 24ε′ + 20√ε′η + 4η2 + (6√ε′ + 2η)∥z1 − z2∥ + ⟨x1 − x2, z1 − z2⟩

+ (√ε′ + η)∥x1 − x2∥2 + (√ε′ + η)∥z1 − z2∥2 + 8√ε′ + 4η − ∥z1 − z2∥2,

2 2

7

---

where we have used (5) in the last inequality with z = x1 − x2 and z = z1 − z2. Next, by noting that (6√ε′ + 2η)∥z1 − z2∥ ≤ 3√ε′ + η + (3√ε′ + η)∥z1 − z2∥, we obtain that

⟨(x1 − z1 − (3√ε′ + η)b1) − (x2 − z2 − (3√ε′ + η)b2), v1 − v2⟩

≤ 24ε′ + 20ε′η + 4η2 + 11ε′ + 5η + (ε′ + η)∥x1 − x2∥2 + ⟨x1 − x2, z1 − z2⟩ − (1 − 4√ε′ − 3η)∥z1 − z2∥2.

Therefore, from inequality (3) and the above calculations, it follows that

−4√ε′ + α ∥v1 − v2∥2 ≤ (4√ε′ + α)⟨ζ1 − ζ2, v1 − v2⟩

= ⟨(x1 − z1 − (3√ε′ + η)b1) − (x2 − z2 − (3√ε′ + η)b2), v1 − v2⟩

≤ 24ε′ + 20ε′η + 4η2 + 11ε′ + 5η + (ε′ + η)∥x1 − x2∥2 + ⟨x1 − x2, z1 − z2⟩ − (1 − 4√ε′ − 3η)∥z1 − z2∥2.

Finally, by using that ∥v1 − v2∥2 ≤ 16ε′ + 16√ε′η + 4η2 + 4√ε′ + 2η + (1 + 4ε′ + 2η)∥z1 − z2∥, we get that

1 − α − 4√ε′ ≤ √ε′ + η ∥x1 − x2∥2 + ⟨x1 − x2, z1 − z2⟩ + (4√ε′ + α)(16ε′ + 16√ε′η + 4η2 + 4√ε′ + 2η) + 20√ε′η + 24ε′ + 11√ε′ + 4η2 + 5η,

which proves the desired inequality.

# 3 Inexact Catching-Up Algorithm for Sweeping Processes

In this section, based on the concept of ε−η projection, we propose an inexact catching-up algorithm for the existence of solutions to the sweeping process:

x˙(t) ∈ −N(C(t); x(t)) + F(t, x(t)) a.e. t ∈ [0, T],

x(0) = x0 ∈ C(0),

where C: [0, T] ⇒ H is a set-valued map with closed values in a Hilbert space H, N(C(t); x) stands for the Clarke normal cone to C(t) at x, and F : [0, T] × H ⇒ H is a given set-valued map with nonempty closed and convex values.

The proposed algorithm is given as follows. For n ∈ N*, let (tn: k = 0, 1, . . . , n) be a uniform partition of [0, T] with uniform time step µ := T /n. Let (εn, ηn) be a sequence of positive numbers such that εn/µ2 → 0 and ηn/µ → 0.

We consider a sequence of piecewise continuous linear approximations (xn) defined as xn(0) = x0 and for any k ∈ {0, . . . , n − 1} and t ∈ ]tn, tn+1],

xn(t) = xn(tk) + (t − tn) / µn (xn − xn(tk) − ∫tktn+1 f(s, xn) ds) + ∫tktn+1 f(s, xn) ds,

where xn = x0 and

xn ∈ projεn,ηn(xn + ∫tktn+1 f(s, xn) ds) for k ∈ {0, 1, . . . , n − 1}.

---

Here f(t, x) denotes any selection of F(t, x) such that f(·, x) is measurable for all x ∈ H. For simplicity, we consider f(t, x) ∈ projγ(0) for some γ > 0.

The above algorithm will be called inexact catching-up algorithm because the projection is not necessarily exactly calculated. We will prove that the above algorithm converges for several families of moving sets as long as inclusion (8) is verified. Let us consider functions δn(·) and θn(·) defined as

|          | if t ∈ \[tn, tn\[ | if t ∈ \[tn, tn\[ |
| -------- | ----------------- | ----------------- |
| δn(t) := | kn                | kn + 1            |
|          | if t = T,         | T                 |

In what follows, we show useful properties of the above algorithm, which will help in proving the existence of solutions for the sweeping process (6) in three cases:
1. The map t ⇒ C(t) takes uniformly prox-regular values.
2. The map t ⇒ C(t) takes subsmooth and ball-compact values.
3. C(t) ≡ C in [0, T] and C is ball-compact.

In what follows, F : [0, T] × H ⇒ H will be a set-valued map with nonempty, closed, and convex values. Moreover, we will consider the following conditions:
- HF1 For all t ∈ [0, T], F(t, ·) is upper semicontinuous from H into Hw.
- HF2 There exists h: H → R+ Lipschitz continuous (with constant Lh > 0) such that

d(0, F(t, x)) := inf{∥w∥ : w ∈ F(t, x)} ≤ h(x) for all x ∈ H and a.e. t ∈ [0, T].
- HF3 There is γ > 0 such that the set-valued map (t, x) ⇒ projγ(0) has a selection f : [0, T] × H → H with f(·, x) is measurable for all x ∈ H.

The following proposition, proved in [11], provides a condition for the feasibility of hypothesis HF3.

Proposition 3.1. Let us assume that H is a separable Hilbert space. Moreover we suppose F(·, x) is measurable for all x ∈ H, then HF3 holds for all γ > 0.

Now, we establish the main properties of the inexact catching-up algorithm.

Theorem 3.2. Assume, in addition to HF1, HF2 and HF3, that C: [0, T] ⇒ H is a set-valued map with nonempty and closed values such that

(9) Haus(C(t), C(s)) ≤ LC∥t − s∥ for all t, s ∈ [0, T].

Then, the sequence of functions (xn : [0, T] → H) generated by numerical scheme (7) and (8) satisfies the following properties:
1. There are non-negative constants K1, K2, K3, K4, K5 such that for all n ∈ N and t ∈ [0, T]:
- (i) dC(θn(t))(xn(δn(t)) + θn(t) f(s, xn(δn(t)))ds) ≤ (LC + h(x(δn(t))) + √γ)μn + ηn.
- (ii) ∥xn(θn(t)) − x0∥ ≤ K1.
- (iii) ∥xn(t)∥ ≤ K2.
- (iv) dC(θn(t))(xn(δn(t)) + θn(t) f(s, xn(δn(t)))ds) ≤ K3μn + ηn.
- (v) ∥xn(θn(t)) − xn(δn(t))∥ ≤ K4μn + √εn + ηn.
- (vi) ∥xn(t) − xn(θn(t))∥ ≤ K5μn + 2√εn + 2ηn.

---

(b) There exists K6 > 0 such that for all t ∈ [0, T] and m, n ∈ N we have

dC(θₙ(t))(xm(t)) ≤ K6µm + LCµn + 2√εm + 3ηm.

(c) There exists K7 > 0 such that for all n ∈ N

∥x˙n(t)∥ ≤ K7 a.e. t ∈ [0, T].

(d) For all n ∈ N and k ∈ {0, 1, . . . , n − 1}, there is vn ∈ C(tn) such that for all t ∈ ]tn, tn[:

λn(t) x˙n(t) ∈ − µn ∂PdC(θₙ(t))(vk+1) + f(t, xn(δn(t))) + µn B.

where λn(t) = 4√σn + (LC + h(xn(δn(t))) + √γ)µn + ηn and σn = 2εn + 2K3ηnµn + 4η2.

Moreover, ∥vn − xn(θn(t))∥ &#x3C; 2√σn + ηn.

Proof. (a): Set µn := T /n and let (εn) and (ηn) be sequences of non-negative numbers such that εn/µ2 → 0 and ηn/µn → 0. We define c := supn∈N √εₙηₙ. We denote by Lₕ the Lipschitz constant of h. For all t ∈ [0, T] and n ∈ N, we define τn(t) := xn(δn(t)) + θₙ(t) f(s, xn(δn(t)))ds.

since distances functions are 1-Lipschitz

(11) dC(θₙ(t))(τn(t)) ≤ dC(θₙ(t))(xn(δn(t))) + ∥f(s, xn(δn(t)))ds∥.

On the one hand, by virtue of (8), we have that xn ∈ C(tn) + ηnB, which implies that for some bn(t) ∈ B, xn(δn(t)) − ηnbn(t) ∈ C(δn(t)). Then,

dC(θₙ(t))(xn(δn(t))) = dC(θₙ(t))(xn(δn(t))) − dC(δn(t))(xn(δn(t)) − ηnbn(t)) ≤ dC(θₙ(t))(xn(δn(t))) − dC(δn(t))(xn(δn(t))) + ∥ηnbn(t)∥.

Then, by using (9) and the fact that Haus(A, B) = supw∈H |dA(w) − dB(w)|, we obtain that

dC(θₙ(t))(xn(δn(t))) ≤ LCµn + ηn.

On the other hand, since f(t, xn(δn(t))) ∈ projγ(0) and HF holds, we get that

∥f(s, xn(δn(t)))∥ ≤ h(xn(δn(t))) + √γ.

Then, it follows from (11) that

dC(θₙ(t))(τn(t)) ≤ LCµn + ηn + θₙ(t)(h(xn(δn(t))) + √γ)ds

≤ (LC + h(xn(δn(t))) + √γ)µn + ηn,

which proves (i). Moreover, since xn(θn(t)) ∈ projεⁿ,ηⁿ(τn(t)), we get that

(12) ∥xn(θn(t)) − τn(t)∥ ≤ dC(θₙ(t))(τn(t))) + √εn

≤ (LC + h(xn(δn(t))) + √γ)µn + ηn + εn,

which yields

(13) ∥xn(θn(t)) − xn(δn(t))∥ ≤ (LC + 2h(xn(δn(t))) + 2√γ)µn + ηn + √εn

≤ (LC + 2h(x0) + 2Lh∥xn(δn(t)) − x0∥ + 2√γ)µn + ηn + εn,

---

where we have used that h is Lipschitz continuous with constant Lh > 0 in the last inequality. Hence for all t ∈ [0, T]

∥xn(θn(t)) − x0∥ ≤ (1 + 2Lhµn)∥xn(θn(t)) − x0∥

+ (LC + 2h(x0) + 2√γ)µn + ηn + εn.

The above inequality means that for all k ∈ {0, 1, . . . , n − 1} :

∥xnk+1 − x0∥ ≤ (1 + 2Lhµn)∥xnk − x0∥ + (LC + 2h(x0) + 2√γ)µn + ηn + √εn.

Then, by [13, p.183], we obtain that for all k ∈ {0, . . . , n − 1}

∥xnk+1 − x0∥ ≤ (k + 1)((LC + 2h(x0) + 2√γ)µn + ηn + √εn) exp(2Lh(k + 1)µn)

(14) ≤ T(LC + 2h(x0) + 2√γ + c) exp(2LhT) =: K1,

which proves (ii).

(iii): By definition of xn, for t ∈]tn, tnk+1] and k ∈ {0, . . . , n − 1}, using (7)

∥xn(t)∥ ≤ ∥xn∥ + ∥xnk − τn(t)∥ + ∫tnk∥f(s, xn)∥ds

≤ K + ∥x0∥ + (L1 + √γ + h(xk))µn + ηn + εn + (h(xk) + γ)µn,

where we have used (12) and (14). Moreover, it is clear that for k ∈ {0, . . . , n}

h(xn) ≤ h(x0) + Lh∥xn − x0∥ ≤ h(x0) + LhK1

Therefore, for all t ∈ [0, T]

∥xn(t)∥ ≤ K1 + ∥x0∥ + (LC + 2(h(x0) + LhK1 + √γ))µn + ηn + √εn

≤ K1 + ∥x0∥ + T(LC + 2(h(x0) + LhK1 + √γ) + c) := K2,

which proves (iii).

(iv) By using the Lipschitz continuity of h, we see that h(x(δn(t)) ≤ h(x0) + Lh∥xn(δn) − x0∥.

Hence, by virtue of (i) and (iii), there exists K3 = (LC + h(x0) + Lh(K2 + ∥x0∥) + √γ) > 0 for which (iv) holds for all n ∈ N.

(v): From (13) and (14) it is easy to see that there exists K4 > 0 such that for all n ∈ N and t ∈ [0, T]: ∥xn(θn(t)) − xn(δn(t))∥ ≤ K4µn + √εn + ηn.

(vi): To conclude this part, we consider t ∈]tn, tnk+1] for some k ∈ {0, . . . , n − 1}.

Then xn(θn(t)) = xnk and also

∥xn(θn(t)) − xn(t)∥ ≤ ∥xnk+1 − xnk∥ + ∥xnk − τn(t)∥ + ∫tnk∥f(s, xn)∥ds

≤ K4µn + √εn + ηn + (LC + √γ + h(x0)+ LhK1)µn + εn + ηn

≤ (K4 + LC + 2(h(x0) + LhK1 + 2√γ))µn + 2εn + 2ηn,

:= K5

and we conclude this first part.

(b): Let m, n ∈ N and t ∈ [0, T], then

dC(θn(t))(xm(t)) ≤ dC(θn(t))(xm(θm(t))) + ∥xm(θm(t)) − xm(t)∥

≤ dC(θn(t))(xm(θm(t))) + K5µm + 2√εm + 2ηm,

11

---

where we have used (v). Since xm ∈ C(tm) + ηmB, we have that xm(θm(t))−ηmbm(t) ∈ C(θm(t)) where bm(t) ∈ B, then we have

k+1

dC(θₙ(t))(xm(θm(t))) = dC(θₙ(t))(xm(θm(t))) − dC(θₘ(t))(xm(θm(t)) − ηmbm(t))

≤ dC(θₙ(t))(xm(θm(t))) − dC(θₘ(t))(xm(θm(t))) + ηm

≤ dH(C(θn(t)), C(θm(t))) + ηm.

Therefore,

dC(θₙ(t))(xm(t)) ≤ dH(C(θn(t)), C(θm(t))) + ηm + K5µm + 2√εm + 2ηm

≤ LC|θn(t) − θm(t)| + K5µm + 2√εm + 3ηm

≤ LC(µn + µm) + K5µm + 2√εm + 3ηm.

Hence, by setting K6 := K5 + LC we proved (b).

(c): Let n ∈ N, k ∈ {0, . . . , n − 1} and t ∈]tn, tk+1]. Then,

∥x˙n(t)∥ = ∥µn (xk+1 − xk − tⁿ f(s, xk )ds) + f(t, xk )∥

≤ 1 ∥xn(θn(t)) − τn(t)∥ + ∥f(t, xn)∥

µn

≤ 1 ((LC + h(xn) + √γ)µn + √εn + ηn) + h(xn) + √γ

µn

≤ √εn + ηn + LC + 2(h(x0) + LhK1 + √γ)

≤  + µn

√c LC + 2(h(x0) + LhK1 + γ) =: K7,

which proves (c).

(d): Fix k ∈ {0, . . . , n − 1} and t ∈]tk , tk+1[. Then,

2.8, there exists vn ∈ C(tn) such that ∥xn − vn∥ &#x3C; 2 ε′ + ηn and

τn(t) − xn ∈ αn(t)∂PdC(tₙ)(vn) + (3 ε′ + ηn)B, ∀t ∈]tn, tn[

where ε′ = εn + 2ηn(dC(tₙ)(τn(t)) + √εn) + η2 and αn(t) = 4 ε′ + dC(θ(t))(τn(t)). We observe that using (iii), we get εn ≤ 2εn + 2K3ηnµn + 4ηn =: σn and σn/µn → 0. By virtue of (i),

αn(t) ≤ 4√σn + (LC + h(xn(δn(t))) + √γ)µn + ηn =: λn(t).

Then, for all t ∈]tn, tn[

−µn (x˙n(t) − f(t, xk )) ∈ λn(t)∂PdC(tₙ₊₁)(vk+1) + (3 σn + ηn)B,

which implies that for t ∈]tn, tn[

x˙n(t) ∈ − µn P C(θₙ(t)) λn(t) ∂dC(vn) + f(t, x(δ(t))) + (3√σn + ηn).

# 4 The Case of Prox-Regular Moving Sets

In this section, we prove the convergence of the inexact catching-up algorithm when the moving sets are uniformly prox-regular. Our results extend the convergence analysis carried out in the classical and inner approximate cases (see [8, 17]).

---

# Theorem 4.1.

Suppose, in addition to the assumptions of Theorem 3.2, that C(t) is ρ-uniformly prox-regular for all t ∈ [0, T], and for all r > 0, there exists a nonnegative integrable function kr such that for all t ∈ [0, T] and x1, x2 ∈ rB one has

(15) ⟨v1 − v2, x1 − x2⟩ ≤ kr(t)∥x1 − x2∥² for all vi ∈ F(t, xi), i = 1, 2.

Then, the sequence of functions (xn) generated by the algorithm (7) and (8) converges uniformly to a Lipschitz continuous solution x(·) of (6). Moreover, if there exists c ∈ L1([0, T]; R+) such that

sup ∥y∥ ≤ c(t)(∥x∥ + 1) for all x ∈ H and a.e. t ∈ [0, T],

y∈F(t,x)

then the solution x(·) is unique.

# Proof.

Consider m, n ∈ N with m ≥ n sufficiently large such that for all t ∈ [0, T], dC(θₙ(t))(xm(t)) &#x3C; ρ, this can be guaranteed by Theorem 3.2. Then, a.e. t ∈ [0, T]

d 1 ∥x˙(t) − x˙(t)∥² = ⟨x˙(t) − x˙(t), xn(t) − xm(t)⟩.

Let t ∈ [0, T] where the above equality holds. Let k, j ∈ {0, 1, ..., n − 1} such that t ∈]tn, tn   ] and t ∈]tm, tm                 ]. On the one hand, we have that

⟨x˙(t) − x˙(t), x(t) − x(t)⟩ = ⟨x˙(t) − x˙(t), xn(t) − xk+1⟩ + ⟨x˙(t) − x˙(t), xk+1 − vk+1⟩ + ⟨x˙(t) − x˙(t), vk+1 − vj+1⟩ + ⟨x˙(t) − x˙(t), vj+1 − xj+1⟩ + ⟨x˙(t) − x˙(t), xj+1 − xm(t)⟩

≤ 2K7K5(µn + µm) + 4K7(√εn + √εm + √σn + √σn) + 6K (η + η) + ⟨x˙(t) − x˙(t), vk+1 − vj+1⟩,

where vn ∈ C(tn) and vm ∈ C(tm) are the given in Theorem 3.2. We can see that

max{dC(tₙ)(vm), dC(tₘ)(vn)} ≤ Haus(C(tm), C(tn)) ≤ LC|tm − tn| ≤ LC(µn + µm).

From now, m, n ∈ N are big enough such that LC(µn + µm) &#x3C; ρ. Moreover, as h is Lh-Lipschitz, we have that for all p ∈ N, i ∈ {0, 1, ..., p} and t ∈ [0, T]

∥f(t, xp)∥ ≤ h(xp) + √γ ≤ h(x0) + LhK1 + √γ =: α.

From the other hand, using (10) and Proposition 2.2 we have that

1 max{ ζ − x˙(t), v − v, ζ − x˙(t), vk+1 − vj+1 } ≤ 2 ∥vn − vm∥² + LC(µn + µm),

where ξn, ξm ∈ B, Γ := sup{ λℓ(t) : t ∈ [0, T], ℓ ∈ N} and ζi := f(t, xi(δi(t))) + 3√σⁱ+ηⁱ ξi for µℓ µi

---

i ∈ {n, m}. Therefore, we have that

⟨xn ˙(t) − xm ˙(t), vk+1 − vj+1⟩

= ⟨xn ˙n(t) − ζn, vk+1 − vj+1⟩ + ⟨ζn − ζm, vk+1 − vj+1⟩

+ ⟨ζm ˙m(t), vk+1 − vj+1⟩

≤ 2Γ( 2 ∥vn − vm∥2 + LC(µn + µm)) + ⟨ζn − ζm, vn − vm⟩

≤ 4Γ (∥xn(t) − xm(t)∥ + 2(√εn + √εm + √σn + √σm) + 3(ηn + ηm) + K5(µn + µm))2

+ 2ΓLC(µn + µm) + ⟨ζn − ζm, vn − vm⟩.

Moreover, using Theorem 3.2 and property (15),

⟨ζn − ζm, vn − vm⟩

= ⟨f(t, xn(δn(t))) − f(t, xm(δm(t))), xn(δn(t)) − xm(δm(t))⟩

+ ⟨f(t, xn(δn(t))) − f(t, xm(δm(t))), vn − xn⟩

+ ⟨f(t, xn(δn(t))) − f(t, xm(δm(t))), xn − xn⟩

+ ⟨f(t, xn(δn(t))) − f(t, xm(δm(t))), xm − xm⟩

+ ⟨f(t, xn(δn(t))) − f(t, xm(δm(t))), xm − vm⟩

+ 3√σn + ηn ⟨ξn, vn − vm⟩ + 3√σm + ηm ⟨ξm, vm − vn⟩

≤ k(t)∥xn(δn(t)) − xm(δm(t))∥2

+ 2α(2(√σn + √σm) + √εn + √εm + 2(ηn + ηm) + K4(µn + µm))

+ 3√σn + ηn ∥vn − vm∥ + 3√σm + ηm ∥vm − vn∥

≤ k(t)(∥xn(t) − xm(t)∥ + 3(εn + √εm) + 3(ηn + ηm + (K4 + K5)(µn + µm))2

+ 2α(2(√σn + √σm) + √εn + √εm + 2(ηn + ηm) + K4(µn + µm))

+ 3√σn + ηn + 3√σm + ηm (2(√σn + √σm) + ηn + ηm + 2K2).

These two inequalities and (16) yield

d ∥xn(t) − xm(t)∥2

dt

≤ 4       4Γ + k(t)          ∥xn(t) − xm(t)∥2

+ 4Kρ                        √      √        √         √

7(K5(µn + µm) + 2(εn + εm + σn + σm) + 3(ηn + ηm)) + 4ΓLC(µn + µm)

+ 4α(2(√σn + √σm) + √εn + √εm + 2(ηn + ηm) + K4(µn + µm))

+ 2       3√σn + ηn + 3√σm + ηm          (2(√σn + √σm) + ηn + ηm + 2K2)

+ 16Γ (2(√εn + √εm + √σn + √σm) + 3(ηn + ηm + K5(µn + µm))2

+ 4k(t) (3(εn + εm) + 3(ηn + ηm) + (K4 + K5)(µn + µm)).

Hence, using Gronwall’s inequality, we have for all t ∈ [0, T] and n, m big enough:

∥xn(t) − xm(t)∥2 ≤ Am,n exp   16Γ T + 4      T k(s)ds     ,

ρ          0

14

---

where,      √      √      √      √

Am,n = 4αT(2(σn + σm) + εn + εm + 2(ηn + ηm) + K4(µn + µm))

+ 4TK7(K5(µn + µm) + 2(√εn + √εm + √σn + √σn) + 3(ηn + ηm))

+ 4TΓLC(µn + µm) + 2T 3√σn + ηn + 3√σm + ηm (2(√σn + √σm) + ηn + ηm + 2K2)

---

# The Case of Uniformly Subsmooth Moving Sets

In this section, we prove the convergence of the inexact catching-up algorithm when the moving sets are uniformly subsmooth. Our results extend the convergence analysis carried out [19, 17]. In contrast to the prox-regular case, uniform subsmoothness fails to guarantee a sufficiently strong monotonicity of the normal cone necessary to ensure the existence and uniqueness of solutions. Consequently, in the subsequent analysis, we shall assume that the moving sets are ball-compact.

# Theorem 5.1.

Suppose, in addition to assumptions of Theorem 3.2, that the family (C(t))t∈[0,T] is equi-uniformly subsmooth and the sets C(t) are ball-compact for all t ∈ [0, T]. Then, the sequence of continuous functions (xn) generated by algorithm (7) and (8) converges uniformly (up to a subsequence) to a Lipschitz continuous solution x(·) of (6).

# Proof.

From Theorem 3.2 we have for all n ∈ N and k ∈ {0, . . . , n − 1}, there is vn ∈ C(tn) such that ∥vn − xn∥ &#x3C; 2√σn + ηn and for all t ∈ ]tn, tn]:

x˙n(t) ∈ − λn(t) µn ∂PdC(θₙ(t))(vk+1) + f(t, xn(δn(t))) + µn B.

where λn(t) = 4√σn + (LC + h(x(δn(t))) + √γ)µn + ηn. We define ν := supn∈N 4√σn + ηn. As h is Lh-Lipschitz it follows that λn(t) ≤ (ν + LC + h(x0) + √γ + LhK1)µn.

Defining vn(t) := vn on ]tn, tn], then for all n ∈ N and almost all t ∈ [0, T]

x˙n(t) ∈ −M ∂PdC(θₙ(t))(vn(t)) + f(t, xn(δn(t))) + µn√B

where M := ν + LC + h(x0) + LhK1 + √γ. Moreover, by Theorem 3.2, we have for all t ∈ [0, T]

(17) dC(t)(xn(t)) ≤ dC(θₙ(t))(xn(t)) + LCµn ≤ (K6 + 2LC)µn + 2√εn + 3ηn.

Next, fix t ∈ [0, T] and define K(t) := {xn(t) : n ∈ N}. We claim that K(t) is relatively compact. Indeed, let xm(t) ∈ K(t) and take ym(t) ∈ ProjC(t)(xm(t)) (the projection exists due to the ball compactness of C(t) and the boundedness of K(t)). Moreover, according to (17) and Theorem 3.2,

∥yn(t)∥ ≤ dC(t)(xn(t)) + ∥xn(t)∥ ≤ (K6 + 2LC)µn + 2√εn + 3ηn + K2.

This entails that yn(t) ∈ C(t) ∩ R B for all n ∈ N for some R > 0. Thus, by the ball compactness of C(t), there exists a subsequence (ymₖ(t)) of (ym(t)) converging to some y(t) as k → +∞. Then,

∥xmₖ(t) − y(t)∥ ≤ dC(t)(xmₖ(t)) + ∥ymₖ(t) − y(t)∥ ≤ (K6 + 2LC)µmₖ + 2√εmₖ + 3ηn + ∥ymₖ(t) − y(t)∥,

which implies that K(t) is relatively compact. Moreover, by Theorem 3.2 that K := (xn) is continuous. Therefore, by virtue of Theorem 3.2, Arzela-Ascoli’s and [20, Lemma 2.2], we obtain the existence of a Lipschitz function x(·) and a subsequence (xj) of (xn) such that

- (i) (xj) converges uniformly to x on [0, T].
- (ii) x˙ ⇀ xj in L1([0, T]; H).
- (iii) xj(θj(t)) → x(t) for all t ∈ [0, T].

---

(iv)    xj (δj (t)) → x(t) for all t ∈ [0, T].

(v)     vj (t) → x(t) for all t ∈ [0, T].

From (17) it is clear that x(t) ∈ C(t) for all t ∈ [0, T]. By Mazur’s Lemma, there is a sequence (yj) such that for all j, y ∈ co(1 xk : k ≥ j) and (yj) converges strongly to xj in L ([0, T]; H). That is

yj (t) ∈ co  −M ∂dC(θn(t))(vn(t)) + MB ∩ F(t, xn(δn(t))) + 3√σn + ηn B : n ≥ j.

On the other hand, there exists (yn,j) which converges to xj almost everywhere in [0, T]. Then, using [17, Lemma 2], [17, Lemma 3] and (H1), we have

xj (t) ∈ −M ∂dC(t)(x(t)) + MB ∩ F(t, x(t)) a.e.

Finally, since ∂dC(t)(x(t)) ⊂ N(C(t); x(t)) for all t ∈ [0, T], it follows that x solves (6).

# 6 The Case of a Fixed Set

In this section, we prove the convergence of the inexact catching-up algorithm for the sweeping process driven by a fixed set:

xj (t) ∈ −N (C; x(t)) + F(t, x(t)) a.e. t ∈ [0, T],

x(0) = x0 ∈ C,

where C ⊂ H and F : [0, T] × H ⇒ H is a set-valued map defined as above. It is worth emphasizing that the above dynamical system is strongly related to the concept of a projected dynamical system (see, e.g., [10]). Our results extend the convergence analysis carried out in the classical and inner approximate cases (see [31, 17]). It is worth to emphasizing that, in this case, no regularity of the set C is required.

# Theorem 6.1.

Let C ⊂ H be a ball-compact set and F : [0, T] × H ⇒ H be a set-valued map satisfying (HF), (H2) and (HF). Then, the sequence of functions (xn) generated by the algorithm converges uniformly (up to a subsequence) to a Lipschitz solution x(·) of (18) such that

∥xj (t)∥ ≤ 2(h(x(t)) + γ) a.e. t ∈ [0, T].

Proof.  We are going to use the properties of Theorem 3.2, where now we have LC = 0. First of all, from Theorem 3.2 we have for all n ∈ N and k ∈ {0, 1, . . . , n − 1}, there is vn ∈ C such that ∥vn − xn∥ &#x3C; 2√σn + ηn and for all t ∈]tn, tn+1] :

xn (t) ∈ −λn ∂PdC(vk+1) + f(t, xn(δn(t))) +  λn B,

where λn(t) = 4√σn + ηn + (h(x(δn(t))) + √γ)λn.

Defining vn(t) := vn on ]tn, tn+1], we get that for all n ∈ N and a.e. t ∈ [0, T]

xn (t) ∈ −λn ∂dC(vn(t)) + (h(t, xn(δn(t))) + √γ)B ∩ F(t, xn(δn(t))) + 3√σn + ηn B.

Moreover, by Theorem 3.2, we have

dC(xn(t)) ≤ K6λn + 2√εn + 3ηn for all t ∈ [0, T].

---

Next, fix t ∈ [0, T] and define K(t) := {xn(t) : n ∈ N}. We claim that K(t) is relatively compact. Indeed, let xm(t) ∈ K(t) and take ym(t) ∈ ProjC(xm(t)) (the projection exists due to the ball compactness of C and the boundedness of K(t)). Moreover, according to the above inequality and Theorem 3.2, ∥yn(t)∥ ≤ dC(xn(t)) + ∥xn(t)∥ ≤ K6µn + 2√εn + 3ηn + K2, which entails that yn(t) ∈ C ∩ R B for all n ∈ N for some R > 0. Thus, by the ball-compactness of C, there exists a subsequence (ymₖ(t)) of (ym(t)) converging to some y(t) as k → +∞. Then,

∥xmₖ(t) − y(t)∥ ≤ dC(xmₖ(t)) + ∥ymₖ(t) − y(t)∥ ≤ K6µmₖ + 2√εmₖ + 3ηmₖ + ∥ymₖ(t) − y(t)∥, which implies that K(t) is relatively compact. Moreover, by Theorem 3.2, the set K := (xn) is equicontinuous. Therefore, by virtue of Theorem 3.2, Arzela-Ascoli’s and [20, Lemma 2.2], we obtain the existence of a Lipschitz function x and a subsequence (xj) of (xn) such that

1. (xj) converges uniformly to x on [0, T].
2. x˙j ⇀ x˙ in L([0, T]; H).
3. xj(θj(t)) → x(t) for all t ∈ [0, T].
4. xj(δj(t)) → x(t) for all t ∈ [0, T].
5. vj(t) → x(t) for all t ∈ [0, T].
6. x(t) ∈ C for all t ∈ [0, T].

By Mazur’s Lemma, there is a sequence (y) such that for all j, yj ∈ co(xj) converges strongly to x˙j : k ≥ j and (yj) in L([0, T]; H). i.e.,

yj(t) ∈ co(−αn∂dC(vn(t)) + βnB ∩ F(t, xn(δn(t))) + 3√σn + ηnB : n ≥ j),

where αn := 4√σⁿ + ηⁿ + h(xn(δn(t))) + √γ and βn := h(xn(δn(t))) + √γ. On the other hand, there exists (y) which converges to x˙ a.e. in [0, T]. Then, using [17, Lemma 2], [17, Lemma 3] and 1), we have

x˙(t) ∈ −(h(x(t)) + γ)∂dC(x(t)) + (h(x(t)) + γ)B ∩ F(t, x(t)) for a.e. t ∈ [0, T].

Finally, since ∂dC(x(t)) ⊂ N(C; x(t)) for all t ∈ [0, T], we obtain that x solves (18).

# 7 An Application to Complementarity Dynamical Systems

In this section, we will apply our enhanced algorithm to complementarity dynamical systems. These systems have garnered increasing attention due to their applications in fields such as mechanics, economics, transportation, control systems and electrical circuits, see e.g., [10, 11, 18]. Complementarity dynamical systems combine ordinary differential equations with complementarity conditions, which can, in turn, be equivalently expressed using variational inequalities or specific differential inclusions, see e.g., [9, 2]. Following [11], let us consider the following class of linear complementarity dynamical systems

(19) x˙(t) = Ax(t) + Bζ(t) + Eu(t)

0 ≤ ζ(t) ⊥ w(t) = Cx(t) + Dζ(t) + Gu(t) + F ≥ 0,

---

where the matrices and vectors A, B, C, D, E, F, G are constant of suitable dimensions, x(t) ∈ Rn, u(t) ∈ Rp, ζ(t) ∈ Rm. We consider the special case where D = 0 and assume the existence of a symmetric, positive-definite matrix P such that P B = C⊤. It was shown in [11] that by defining R = √P and introducing the change of variables z(t) = Rx(t), the system (19) can be reformulated as the following perturbed sweeping process:

z˙(t) ∈ −N(S(t); z(t)) + RAR z(t) + REu(t),

where S(t) := R(K(t)) = {Rx : x ∈ K(t)} and K(t) is the closed convex polyhedral set

K(t) := {x ∈ Rn | Cx + Gu(t) + F ≥ 0}.

Fix x ∈ H and ε, η > 0. To apply the inexact catching-up algorithm, we must devise a numerical method to find ε−η approximate projections. Since obtaining the projection involves a quadratically constrained problem, we will use the primal-dual approach (see, e.g., [5]) to the (primal) optimization problem:

(20) d2(x) = infy∈K(t) ∥x − Ry∥2 = infA y ≤ b y⊤P y + 2f⊤y

where Q := P, f := −Rx, A := −C and b := Gu(t) + F. The dual formulation of (20) is

(21) maxλ∈Rm+ − λ⊤AQ−1A⊤λ − 2(AQ−1f + b)⊤λ − f⊤Q−1f.

Moreover, the primal and dual problems are linked through the relation:

(22) y* = −Q−1(f + A⊤λ*),

where y* and λ* are the primal and dual solutions, respectively. Hence, we can solve the dual problem using the projected gradient descent method:

(23) λk+1 = λk − λmax(CB) (CBλk + B⊤Rx + Gu(t) + F),

where [·]+ denotes the projection onto the nonnegative orthant (see, e.g., [4, Lemma 6.26]). Finally, the primal solution can be recovered through relation (22).

# Remark 7.1.

Here, the contribution of our inexact method can be clearly observed. It is easy to see that the proposed algorithm for calculating the projection does not necessarily yield points that remain within the set, highlighting the importance of approaching the projection from any point. The next result provides some properties of the proposed numerical method.

# Lemma 7.2.

Let y* and λ* be solutions of (20) and (21), respectively. Let (λk) be the sequence generated by (23). Define yk = Bλk + R−1x for all k ∈ N. Then, the following assertions hold:

- (i) For all k ∈ N, ∥yk − y*∥ ≤ ∥B∥∥λk − λ*∥.
- (ii) ε, η > 0 Let ¯λ and suppose that, for some k ∈ N, the following condition hold:

∥λ¯ − λ*∥ ≤ max{ ε , η } with M := supk∈N ∥P∥∥B(λk + λ*) + 2R−1x∥ + 2∥Rx∥ ∥B∥.

Then, z := Ry¯ ∈ projε,η(x).

---

Proof. Assertion (i) follows directly from relation (22). To prove (ii), we observe that

∥x − Ryk∥2 − ∥x − Ry*∥2 = y⊤P yk − y*⊤P y* − 2(Rx)⊤(yk − y*)

(24) = (yk + y*)⊤P(yk − y*) + 2(−Rx)⊤(yk − y*)

≤ (∥P∥∥yk + y*∥ + 2∥Rx∥) ∥yk − y*∥

≤ ∥P∥∥B(λk + λ*) + 2R−1x∥ + 2∥Rx∥ ∥B∥∥λk − λ*∥,

where we have used (i). Since the dual problem is a strictly convex quadratic program, (λk) converges to the unique solution λ*, and therefore M &#x3C; +∞. Hence, by using that ∥λk − λ*∥ ≤ ε/M, we obtain that ∥x − Ryk∥2 ≤ d2(x) + ε. Moreover, since ∥λk − λ*∥ ≤ η, it follows from (i) that

∥y* − y∥ ≤ ∥R∥,

which implies that z ∈ projε,η(x).

It is worth mentioning that the number of iterations required to achieve a certain precision (and ensure an ε − η approximate projection) can be estimated using classical results from the projected gradient method (see, e.g., [26, Theorem 2.2.8]). We end this section by applying our numerical method to a problem involving electrical circuits with ideal diodes. The example was considered previously in [2, Example 2.52].

# Example 7.3.

Let us consider the electrical circuit with ideal diodes shown in Figure 1.

Figure 1: Electrical circuit with ideal diodes.

Here R1, R2, R3 ≥ 0, L2, L3 > 0, C4 > 0. The presence of the diodes generates the complementarity relationships 0 ≤ −uD₄ ⊥ x2 ≥ 0 and 0 ≤ −uD₁ ⊥ −x3 + x2 ≥ 0, where uD₄ and uD₁ are the voltages of the diodes. The dynamics of the circuit are given by the following system:

x1(t) = x2(t)

x2(t) = −(R1 + R3)−1L3x2(t) + L1x3(t) − L4x1(t) + L3ζ1(t) + L3ζ2(t) + L3

x3(t) = −(R1 + R2)−1L2x3(t) + L1x2(t) − L2ζ1(t) + L2

0 ≤ ζ1(t) ⊥ −x3(t) + x2(t) ≥ 0,

ζ2(t) x2(t)

where x1(·) is the time integral of the current across the capacitor, x2(·) is the current across the capacitor, and x3(·) is the current across the inductor L2 and resistor R2, −ζ1 is the voltage of the diode D1 and −ζ2 is the voltage of the diode D4. The system in (25) can be written compactly as

x˙(t) = Ax(t) + Bζ(t) + Eu(t)

0 ≤ ζ(t) ⊥ y(t) = Cx(t) ≥ 0,

---

with

| 0      | 1  | 0      | 0  | 0 | 1   | −1 | 0 |    |     |   |     |   |   |
| ------ | -- | ------ | -- | - | --- | -- | - | -- | --- | - | --- | - | - |
| A = −L | 1  | −R¹+R³ | R1 | , | B = | 1  | 1 | ,  | C = | , | E = | 1 | , |
| 3C4    | L3 |        | L3 |   | 0   | 1  | 0 | L3 |     |   |     |   |   |
| 0      | R1 | −R¹+R² | −1 | 0 |     | 1  |   | L2 |     |   |     |   |   |
|        | L2 |        | L2 |   | L2  |    |   |    |     |   |     |   |   |

which is a particular case of (19) with D = 0, F = 0 and G = 0. Moreover, P B = CT holds with

|     | 1     | 0 | 0  |   |     |
| --- | ----- | - | -- | - | --- |
| P = | 0     | L | 0  |   |     |
|     | 0     | 3 | L2 |   |     |
|     | ⇒ R = | 0 | 0  | 3 | √L₂ |

To apply the inexact catching-up algorithm, we consider n = 100, a uniform partition (tn)n of [0, 1] with µ = 1, ε = 1, η = 1. As discussed earlier, the variable z = Rxk satisfies:

z˙(t) ∈ −N(S; z(t)) + f(t, z(t)),

where f(t, x) = RAR−1x + REu(t), S = {Rx : x ∈ K} and K := {x ∈ R3 : −Cx ≤ 0}. We apply the inexact catching-up algorithm by computing for each k ∈ {0, . . . , n − 1}

zn ∈ projεⁿ,ηⁿ(zn + RAR−1znµn + REku(s)ds).

Hence, we consider for each k ∈ {0, 1, . . . , n − 1} the associated dual problem

min λ⊤CBλ + 2 B⊤Rwn⊤λ,

λ∈Rm+

where wn := zn + RAR−1znµ + REktn+1u(s)ds (the integral is evaluated through a classical integration technique). We apply the projected gradient descent (see algorithm (23))

λj+1 = λj − 1 CBλj + B⊤Rwn,

to get an approximate dual solution. Then, from (22), we obtain an approximate primal solution yk. Finally, zk+1 := Ryk satisfies (26).

Figure 2 shows the numerical result for R1 = 1, R2 = 2, R3 = 1, L2 = 1, L3 = 2, C4 = 1, u(t) = 16 sin(6πt) − 0.5 and initial condition x0 = (0, 0, 0).

It is worth noting that the above example is a particular case of (19) with G = 0. The case where G = 0 is especially interesting, as it causes the set K(t) := {x ∈ Rn : Cx + Gu(t) + F ≥ 0} to vary over time. This falls within the scope of our results as long as u(t) is Lipschitz. However, if u(t) is discontinuous, then K(t) will also be discontinuous, and solutions will be discontinuous as well. Although the discontinuous case is not addressed by the developments of this work, the inexact catching algorithm seems to be effective, as is shown in Figure 3.

---

# Figure 2

On the left solution x1 and on the right solutions x2 (black) and x3 (blue) for R1 = 1, R2 = 2, R3 = 1, L2 = 1, L3 = 2, C4 = 1, u(t) = 16 sin(6πt) − 0.5 and x0 = (0, 0, 0).

| 0.5 | 1   |      |     |     |   |    |   |     |     |     |     |   |
| --- | --- | ---- | --- | --- | - | -- | - | --- | --- | --- | --- | - |
| 0.4 | 0.6 |      |     |     |   |    |   |     |     |     |     |   |
| 0.3 | 0.2 |      |     |     |   |    |   |     |     |     |     |   |
| 0.2 |     | −⁰.2 |     |     |   |    |   |     |     |     |     |   |
| 0.1 |     | −⁰.6 |     |     |   |    |   |     |     |     |     |   |
| 0   | 0   |      |     |     |   |    |   |     |     |     |     |   |
|     | 0.2 | 0.4  | 0.6 | 0.8 | 1 | −¹ | 0 | 0.2 | 0.4 | 0.6 | 0.8 | 1 |

# Figure 3

On the left solution x1 and on the right solutions x2 (black) and x3 (blue) for R1 = 1, R2 = 2, R3 = 1, L2 = 1, L3 = 2, C4 = 1, G = (0, 1)t, u(t) = sign(sin(4πt)) and x0 = (0, 0, 0).

|   | 1   | 1    |      |     |   |    |   |     |     |     |     |   |
| - | --- | ---- | ---- | --- | - | -- | - | --- | --- | --- | --- | - |
|   | 0.6 | 0.6  |      |     |   |    |   |     |     |     |     |   |
|   | 0.2 | 0.2  |      |     |   |    |   |     |     |     |     |   |
|   |     | −⁰.2 | −⁰.2 |     |   |    |   |     |     |     |     |   |
|   |     | −⁰.6 | −⁰.6 |     |   |    |   |     |     |     |     |   |
|   |     | −¹   | 0    |     |   |    |   |     |     |     |     |   |
|   | 0.2 | 0.4  | 0.6  | 0.8 | 1 | −¹ | 0 | 0.2 | 0.4 | 0.6 | 0.8 | 1 |

---

# 8 Concluding Remarks

In this paper, we present an inexact version of the catching-up algorithm for sweeping processes. Building on the work in [11], we define a new notion of approximate projection, called ε − η - proximate projection, which is compatible with any numerical method for approximating exact projections, as this new notion is not restricted to remain strictly within the set. We provide several properties of ε− η approximate projections, which enable us to prove the convergence of the inexact catching-up algorithm in three general frameworks: prox-regular moving sets, subsmooth moving sets, and merely closed sets.

Additionally, we apply our numerical results to address complementarity dynamical systems, particularly electrical circuits with ideal diodes. In this context, we implement the inexact - up algorithm using a primal-dual method, which typically does not guarantee a feasible point.

Future research could focus on extending the results of this paper to encompass additional applications, such as crowd motion, as well as cases involving discontinuous moving sets.

# References

1. Acary, V., Bonnefon, O., Brogliato, B.: Nonsmooth modeling and simulation for switched circuits, Lect. Notes Electr. Eng., vol. 69. Springer, Dordrecht (2011)
2. Acary, V., Brogliato, B.: Numerical Methods for Nonsmooth Dynamical Systems: Applications in Mechanics and Electronics. Lect. Notes Appl. Comput. Mech. Springer Berlin Heidelberg (2008)
3. Aussel, D., Daniilidis, A., Thibault, L.: Subsmooth sets: functional characterizations and related concepts. Trans. Amer. Math. Soc. 357(4), 1275–1301 (2005)
4. Beck, A.: First-order methods in optimization, MOS-SIAM Ser. Optim., vol. 25. Society for Industrial and Applied Mathematics (SIAM), Philadelphia, PA; Mathematical Optimization Society, Philadelphia, PA (2017)
5. Beck, A.: Introduction to nonlinear optimization—theory, algorithms, and applications with Python and MATLAB, MOS-SIAM Ser. Optim., vol. 32. Society for Industrial and Applied Mathematics (SIAM), Philadelphia, PA; Mathematical Optimization Society, Philadelphia, PA (2023)
6. Bounkhel, M.: Regularity concepts in nonsmooth analysis, Springer Optim. Appl., vol. 59. Springer, New York (2012)
7. Bounkhel, M., Thibault, L.: On various notions of regularity of sets in nonsmooth analysis. Nonlinear Anal. 48(2), 223–246 (2002)
8. Bounkhel, M., Thibault, L.: Nonconvex sweeping process and prox-regularity in Hilbert space. J. Nonlinear Convex Anal. 6(2), 359–374 (2005)
9. Brogliato, B.: Nonsmooth mechanics, third edn. Commun. Numer. Methods Eng. Springer, [Cham] (2016). Models, dynamics and control
10. Brogliato, B., Daniilidis, A., Lemar´echal, C., Acary, V.: On the equivalence between - mentarity systems, projected systems and differential inclusions. Systems Control Lett. 55(1), 45–51 (2006)
11. Brogliato, B., Thibault, L.: Existence and uniqueness of solutions for non-autonomous - mentarity dynamical systems. J. Convex Anal. 17(3-4), 961–990 (2010)

---

# References

1. Clarke, F.H.: Optimization and nonsmooth analysis, Classics Appl. Math., vol. 5, second edn. Society for Industrial and Applied Mathematics (SIAM), Philadelphia, PA (1990)
2. Clarke, F.H., Ledyaev, Y.S., Stern, R.J., Wolenski, P.R.: Nonsmooth analysis and control theory, Grad. Texts in Math., vol. 178. Springer-Verlag, New York (1998)
3. Colombo, G., Thibault, L.: Prox-regular sets and applications. In: Handbook of nonconvex analysis and applications, pp. 99–182. Int. Press, Somerville, MA (2010)
4. Deimling, K.: Multivalued differential equations, De Gruyter Ser. Nonlinear Anal. Appl., vol. 1. Walter de Gruyter &#x26; Co., Berlin (1992)
5. Federer, H.: Curvature measures. Trans. Amer. Math. Soc. 93, 418–491 (1959)
6. Garrido, J.G., Vilches, E.: Catching-Up Algorithm with Approximate Projections for Moreau’s Sweeping Processes. J. Optim. Theory Appl. 203(2), 1160–1187 (2024)
7. Goeleven, D., Brogliato, B.: Stability and instability matrices for linear evolution variational inequalities. IEEE Trans. Automat. Control 49(4), 521–534 (2004)
8. Haddad, T., Noel, J., Thibault, L.: Perturbed sweeping process with a subsmooth set depending on the state. Linear Nonlinear Anal. 2(1), 155–174 (2016)
9. Jourani, A., Vilches, E.: Moreau-Yosida regularization of state-dependent sweeping processes with nonregular sets. J. Optim. Theory Appl. 173(1), 91–116 (2017)
10. Maury, B., Venel, J.: Un modèle de mouvements de foule. In: Paris-Sud Working Group on Modelling and Scientific Computing 2006–2007, ESAIM Proc., vol. 18, pp. 143–152. EDP Sci., Les Ulis (2007)
11. Moreau, J.J.: Rafle par un convexe variable. I. In: Travaux du Séminaire d’Analyse Convexe, Vol. I, Secrétariat des Mathématiques, Publication, No. 118, pp. Exp. No. 15, 43. Univ. Sci. Tech. Languedoc, Montpellier (1971)
12. Moreau, J.J.: Rafle par un convexe variable. II. In: Travaux du Séminaire d’Analyse Convexe, Vol. II, Secrétariat des Mathématiques, Publication, No. 122, pp. Exp. No. 3, 36. Univ. Sci. Tech. Languedoc, Montpellier (1972)
13. Moreau, J.J.: An introduction to Unilateral Dynamics, pp. 1–46. Springer Berlin Heidelberg (2004). DOI 10.1007/978-3-540-45287-4 1
14. Moreau, J.J.: On Unilateral Constraints, Friction and Plasticity, p. 171–322. Springer Berlin Heidelberg (2011). DOI 10.1007/978-3-642-10960-7 7
15. Nesterov, Y.: Introductory lectures on convex optimization, Applied Optimization, vol. 87. Kluwer Academic Publishers, Boston, MA (2004). A basic course
16. Noel, J., Thibault, L.: Nonconvex sweeping process with a moving set depending on the state. Vietnam J. Math. 42(4), 595–612 (2014)
17. Papageorgiou, N.S., Kyritsi-Yiallourou, S.T.: Handbook of applied analysis, Adv. Mech. Math., vol. 19. Springer, New York (2009)
18. Poliquin, R.A., Rockafellar, R.T., Thibault, L.: Local differentiability of distance functions. Trans. Amer. Math. Soc. 352(11), 5231–5249 (2000)
19. Thibault, L.: Unilateral variational analysis in Banach spaces. Part II—special classes of - tions and sets. World Scientific Publishing Co. Pte. Ltd., Hackensack, NJ (2023)
20. Vilches, E.: Existence and Lyapunov pairs for the perturbed sweeping process governed by a fixed set. Set-Valued Var. Anal. 27(2), 569–583 (2019)
