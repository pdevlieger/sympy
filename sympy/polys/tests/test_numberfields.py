"""Tests for computational algebraic number field theory. """

from sympy import S, Rational, Symbol, Poly, raises, sin, sqrt, I

from sympy.polys.numberfields import (
    minimal_polynomial, primitive_element,
    field_isomorphism, to_number_field,
    AlgebraicNumber,
)

from sympy.polys.polyerrors import (
    IsomorphismFailed,
    NotAlgebraic,
)

from sympy.polys.polyclasses import DMP
from sympy.polys.algebratools import QQ

from sympy.abc import x, y

def test_minimal_polynomial():
    assert minimal_polynomial(-7, x) == x + 7
    assert minimal_polynomial(-1, x) == x + 1
    assert minimal_polynomial( 0, x) == x
    assert minimal_polynomial( 1, x) == x - 1
    assert minimal_polynomial( 7, x) == x - 7

    assert minimal_polynomial(sqrt(2), x) == x**2 - 2
    assert minimal_polynomial(sqrt(5), x) == x**2 - 5
    assert minimal_polynomial(sqrt(6), x) == x**2 - 6

    assert minimal_polynomial(2*sqrt(2), x) == x**2 - 8
    assert minimal_polynomial(3*sqrt(5), x) == x**2 - 45
    assert minimal_polynomial(4*sqrt(6), x) == x**2 - 96

    assert minimal_polynomial(2*sqrt(2) + 3, x) == x**2 -  6*x +  1
    assert minimal_polynomial(3*sqrt(5) + 6, x) == x**2 - 12*x -  9
    assert minimal_polynomial(4*sqrt(6) + 7, x) == x**2 - 14*x - 47

    assert minimal_polynomial(2*sqrt(2) - 3, x) == x**2 +  6*x +  1
    assert minimal_polynomial(3*sqrt(5) - 6, x) == x**2 + 12*x -  9
    assert minimal_polynomial(4*sqrt(6) - 7, x) == x**2 + 14*x - 47

    assert minimal_polynomial(sqrt(1 + sqrt(6)), x) == x**4 -  2*x**2 -  5
    assert minimal_polynomial(sqrt(I + sqrt(6)), x) == x**8 - 10*x**4 + 49

    assert minimal_polynomial(2*I + sqrt(2 + I), x) == x**4 + 4*x**2 + 8*x + 37

    assert minimal_polynomial(sqrt(2) + sqrt(3), x) == x**4 - 10*x**2 + 1
    assert minimal_polynomial(sqrt(2) + sqrt(3) + sqrt(6), x) == x**4 - 22*x**2 - 48*x - 23

    a = 1 - 9*sqrt(2) + 7*sqrt(3)

    assert minimal_polynomial(1/a, x) == 392*x**4 - 1232*x**3 + 612*x**2 + 4*x - 1
    assert minimal_polynomial(1/sqrt(a), x) == 392*x**8 - 1232*x**6 + 612*x**4 + 4*x**2 - 1

    raises(NotAlgebraic, "minimal_polynomial(y, x)")
    raises(NotAlgebraic, "minimal_polynomial(2**y, x)")
    raises(NotAlgebraic, "minimal_polynomial(sin(1), x)")

    assert minimal_polynomial(sqrt(2), polys=True).is_Poly == True
    assert minimal_polynomial(sqrt(2), x, polys=True) == Poly(x**2 - 2)

    a = AlgebraicNumber(sqrt(2))
    b = AlgebraicNumber(sqrt(3))

    assert minimal_polynomial(a, x) == x**2 - 2
    assert minimal_polynomial(b, x) == x**2 - 3

    assert minimal_polynomial(a, x, polys=True) == Poly(x**2 - 2)
    assert minimal_polynomial(b, x, polys=True) == Poly(x**2 - 3)

    assert minimal_polynomial(sqrt(a/2 + 17), x) == 2*x**4 -  68*x**2 +  577
    assert minimal_polynomial(sqrt(b/2 + 17), x) == 4*x**4 - 136*x**2 + 1153

    a, b = sqrt(2)/3 + 7, AlgebraicNumber(sqrt(2)/3 + 7)

    f = 81*x**8 - 2268*x**6 - 4536*x**5 + 22644*x**4 + 63216*x**3 - 31608*x**2 - 189648*x + 141358

    assert minimal_polynomial(sqrt(a) + sqrt(sqrt(a)), x) == f
    assert minimal_polynomial(sqrt(b) + sqrt(sqrt(b)), x) == f

    assert minimal_polynomial(a**Rational(3, 2), x) == 729*x**4 - 506898*x**2 + 84604519

def test_primitive_element():
    assert primitive_element([sqrt(2), sqrt(3)], x) == (x**4 - 10*x**2 + 1, sqrt(2) + sqrt(3))
    assert primitive_element([sqrt(2), sqrt(3)], x, polys=True) == (Poly(x**4 - 10*x**2 + 1), sqrt(2) + sqrt(3))

    raises(ValueError, "primitive_element([], x)")

def test_field_isomorphism():
    assert field_isomorphism(3, sqrt(2)) == [3]

    assert field_isomorphism( I*sqrt(3), I*sqrt(3)/2) == [ 2, 0]
    assert field_isomorphism(-I*sqrt(3), I*sqrt(3)/2) == [-2, 0]

    assert field_isomorphism( I*sqrt(3),-I*sqrt(3)/2) == [-2, 0]
    assert field_isomorphism(-I*sqrt(3),-I*sqrt(3)/2) == [ 2, 0]

    assert field_isomorphism( 2*I*sqrt(3)/7, 5*I*sqrt(3)/3) == [ S(6)/35, 0]
    assert field_isomorphism(-2*I*sqrt(3)/7, 5*I*sqrt(3)/3) == [-S(6)/35, 0]

    assert field_isomorphism( 2*I*sqrt(3)/7,-5*I*sqrt(3)/3) == [-S(6)/35, 0]
    assert field_isomorphism(-2*I*sqrt(3)/7,-5*I*sqrt(3)/3) == [ S(6)/35, 0]

    assert field_isomorphism( 2*I*sqrt(3)/7+27, 5*I*sqrt(3)/3) == [ S(6)/35, 27]
    assert field_isomorphism(-2*I*sqrt(3)/7+27, 5*I*sqrt(3)/3) == [-S(6)/35, 27]

    assert field_isomorphism( 2*I*sqrt(3)/7+27,-5*I*sqrt(3)/3) == [-S(6)/35, 27]
    assert field_isomorphism(-2*I*sqrt(3)/7+27,-5*I*sqrt(3)/3) == [ S(6)/35, 27]

    p = AlgebraicNumber( sqrt(2) + sqrt(3))
    q = AlgebraicNumber(-sqrt(2) + sqrt(3))
    r = AlgebraicNumber( sqrt(2) - sqrt(3))
    s = AlgebraicNumber(-sqrt(2) - sqrt(3))

    pos_coeffs = [ S(1)/2, S(0), -S(9)/2, S(0)]
    neg_coeffs = [-S(1)/2, S(0),  S(9)/2, S(0)]

    a = AlgebraicNumber(sqrt(2))

    assert field_isomorphism(a, p) == pos_coeffs
    assert field_isomorphism(a, q) == neg_coeffs
    assert field_isomorphism(a, r) == pos_coeffs
    assert field_isomorphism(a, s) == neg_coeffs

    a = AlgebraicNumber(-sqrt(2))

    assert field_isomorphism(a, p) == neg_coeffs
    assert field_isomorphism(a, q) == pos_coeffs
    assert field_isomorphism(a, r) == neg_coeffs
    assert field_isomorphism(a, s) == pos_coeffs

    pos_coeffs = [ S(1)/2, S(0), -S(11)/2, S(0)]
    neg_coeffs = [-S(1)/2, S(0),  S(11)/2, S(0)]

    a = AlgebraicNumber(sqrt(3))

    assert field_isomorphism(a, p) == neg_coeffs
    assert field_isomorphism(a, q) == neg_coeffs
    assert field_isomorphism(a, r) == pos_coeffs
    assert field_isomorphism(a, s) == pos_coeffs

    a = AlgebraicNumber(-sqrt(3))

    assert field_isomorphism(a, p) == pos_coeffs
    assert field_isomorphism(a, q) == pos_coeffs
    assert field_isomorphism(a, r) == neg_coeffs
    assert field_isomorphism(a, s) == neg_coeffs

    pos_coeffs = [ S(3)/2, S(0), -S(33)/2, -S(8)]
    neg_coeffs = [-S(3)/2, S(0),  S(33)/2, -S(8)]

    a = AlgebraicNumber(3*sqrt(3)-8)

    assert field_isomorphism(a, p) == neg_coeffs
    assert field_isomorphism(a, q) == neg_coeffs
    assert field_isomorphism(a, r) == pos_coeffs
    assert field_isomorphism(a, s) == pos_coeffs

    a = AlgebraicNumber(3*sqrt(2)+2*sqrt(3)+1)

    assert field_isomorphism(a, p) == [ S(1)/2, S(0), -S(5)/2,  S(1)]
    assert field_isomorphism(a, q) == [-S(5)/2, S(0),  S(49)/2, S(1)]
    assert field_isomorphism(a, r) == [ S(5)/2, S(0), -S(49)/2, S(1)]
    assert field_isomorphism(a, s) == [-S(1)/2, S(0),  S(5)/2,  S(1)]

    assert field_isomorphism(sqrt(2), sqrt(3)) is None
    assert field_isomorphism(sqrt(3), sqrt(2)) is None

def test_to_number_field():
    assert to_number_field(sqrt(2)) == AlgebraicNumber(sqrt(2))
    assert to_number_field([sqrt(2), sqrt(3)]) == AlgebraicNumber(sqrt(2)+sqrt(3))

    a = AlgebraicNumber(sqrt(2)+sqrt(3), [S(1)/2, S(0), -S(9)/2, S(0)])

    assert to_number_field(sqrt(2), sqrt(2)+sqrt(3)) == a
    assert to_number_field(sqrt(2), AlgebraicNumber(sqrt(2)+sqrt(3))) == a

    raises(IsomorphismFailed, "to_number_field(sqrt(2), sqrt(3))")

def test_AlgebraicNumber():
    minpoly, root = x**2 - 2, sqrt(2)

    a = AlgebraicNumber(root, gen=x)

    assert a.rep == DMP([QQ(1),QQ(0)], QQ)
    assert a.root == root
    assert a.alias is None
    assert a.minpoly == minpoly

    assert a.is_aliased == False

    assert a.coeffs() == [S(1), S(0)]
    assert a.native_coeffs() == [QQ(1), QQ(0)]

    a = AlgebraicNumber(root, gen=x, alias='y')

    assert a.rep == DMP([QQ(1),QQ(0)], QQ)
    assert a.root == root
    assert a.alias == Symbol('y')
    assert a.minpoly == minpoly

    assert a.is_aliased == True

    a = AlgebraicNumber(root, gen=x, alias=Symbol('y'))

    assert a.rep == DMP([QQ(1),QQ(0)], QQ)
    assert a.root == root
    assert a.alias == Symbol('y')
    assert a.minpoly == minpoly

    assert a.is_aliased == True

    assert AlgebraicNumber(sqrt(2), []).rep == DMP([], QQ)

    assert AlgebraicNumber(sqrt(2), [8]).rep == DMP([QQ(8)], QQ)
    assert AlgebraicNumber(sqrt(2), [S(8)/3]).rep == DMP([QQ(8,3)], QQ)

    assert AlgebraicNumber(sqrt(2), [7, 3]).rep == DMP([QQ(7),QQ(3)], QQ)
    assert AlgebraicNumber(sqrt(2), [S(7)/9, S(3)/2]).rep == DMP([QQ(7,9),QQ(3,2)], QQ)

    assert AlgebraicNumber(sqrt(2), [1, 2, 3]).rep == DMP([QQ(2),QQ(5)], QQ)

    a = AlgebraicNumber(AlgebraicNumber(root, gen=x), [1,2])

    assert a.rep == DMP([QQ(1),QQ(2)], QQ)
    assert a.root == root
    assert a.alias is None
    assert a.minpoly == minpoly

    assert a.is_aliased == False

    assert a.coeffs() == [S(1), S(2)]
    assert a.native_coeffs() == [QQ(1), QQ(2)]

    a = AlgebraicNumber((minpoly, root), [1,2])

    assert a.rep == DMP([QQ(1),QQ(2)], QQ)
    assert a.root == root
    assert a.alias is None
    assert a.minpoly == minpoly

    assert a.is_aliased == False

    a = AlgebraicNumber((Poly(minpoly), root), [1,2])

    assert a.rep == DMP([QQ(1),QQ(2)], QQ)
    assert a.root == root
    assert a.alias is None
    assert a.minpoly == minpoly

    assert a.is_aliased == False

    assert AlgebraicNumber( sqrt(3)).rep == DMP([ QQ(1),QQ(0)], QQ)
    assert AlgebraicNumber(-sqrt(3)).rep == DMP([-QQ(1),QQ(0)], QQ)

    a = AlgebraicNumber(sqrt(2))
    b = AlgebraicNumber(sqrt(2))

    assert a == b and a == sqrt(2)

    a = AlgebraicNumber(sqrt(2), gen=x)
    b = AlgebraicNumber(sqrt(2), gen=x)

    assert a == b and a == sqrt(2)

    a = AlgebraicNumber(sqrt(2), [1,2])
    b = AlgebraicNumber(sqrt(2), [1,3])

    assert a != b and a != sqrt(2)+3

    assert (a == x) == False and (a != x) == True

    a = AlgebraicNumber(sqrt(2), [1,0])
    b = AlgebraicNumber(sqrt(2), [1,0], alias=y)

    assert a.as_poly(x) == Poly(x)
    assert b.as_poly()  == Poly(y)

    assert a.as_basic()  == sqrt(2)
    assert a.as_basic(x) == x
    assert b.as_basic()  == sqrt(2)
    assert b.as_basic(x) == x

    a = AlgebraicNumber(sqrt(2), [2,3])
    b = AlgebraicNumber(sqrt(2), [2,3], alias=y)

    p = a.as_poly()

    assert p == Poly(2*p.gen+3)

    assert a.as_poly(x) == Poly(2*x+3)
    assert b.as_poly()  == Poly(2*y+3)

    assert a.as_basic()  == 2*sqrt(2)+3
    assert a.as_basic(x) == 2*x+3
    assert b.as_basic()  == 2*sqrt(2)+3
    assert b.as_basic(x) == 2*x+3

def test_to_algebraic_integer():
    a = AlgebraicNumber(sqrt(3), gen=x).to_algebraic_integer()

    assert a.minpoly == x**2 - 3
    assert a.root    == sqrt(3)
    assert a.rep     == DMP([QQ(1),QQ(0)], QQ)

    a = AlgebraicNumber(2*sqrt(3), gen=x).to_algebraic_integer()

    assert a.minpoly == x**2 - 12
    assert a.root    == 2*sqrt(3)
    assert a.rep     == DMP([QQ(1),QQ(0)], QQ)

    a = AlgebraicNumber(sqrt(3)/2, gen=x).to_algebraic_integer()

    assert a.minpoly == x**2 - 12
    assert a.root    == 2*sqrt(3)
    assert a.rep     == DMP([QQ(1),QQ(0)], QQ)

    a = AlgebraicNumber(sqrt(3)/2, [S(7)/19, 3], gen=x).to_algebraic_integer()

    assert a.minpoly == x**2 - 12
    assert a.root    == 2*sqrt(3)
    assert a.rep     == DMP([QQ(7,19),QQ(3)], QQ)
