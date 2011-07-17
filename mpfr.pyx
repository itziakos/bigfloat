# GMP type declarations
cdef extern from "gmp.h":
    ctypedef int mp_exp_t
    ctypedef unsigned int mp_limb_t

# MPFR type declarations
cdef extern from "mpfr.h":
    ctypedef int mpfr_prec_t
    ctypedef int mpfr_sign_t
    ctypedef mp_exp_t mpfr_exp_t

    ctypedef struct __mpfr_struct:
        mpfr_prec_t _mpfr_prec
        mpfr_sign_t _mpfr_sign
        mpfr_exp_t  _mpfr_exp
        mp_limb_t   *_mpfr_d

    ctypedef __mpfr_struct mpfr_t[1]

    ctypedef enum mpfr_rnd_t:
        C_MPFR_RNDN "MPFR_RNDN" = 0
        C_MPFR_RNDZ "MPFR_RNDZ"
        C_MPFR_RNDU "MPFR_RNDU"
        C_MPFR_RNDD "MPFR_RNDD"
        C_MPFR_RNDA "MPFR_RNDA"
        C_MPFR_RNDF "MPFR_RNDF"
        C_MPFR_RNDNA "MPFR_RNDNA" = -1

    # MPFR function definitions
    void c_mpfr_init2 "mpfr_init2" (mpfr_t x, mpfr_prec_t prec)
    void c_mpfr_clear "mpfr_clear" (mpfr_t x)

    char * c_mpfr_get_str "mpfr_get_str" (
        char *str, mpfr_exp_t *expptr, int b,
        size_t n, mpfr_t op, mpfr_rnd_t rnd
    )

    void c_mpfr_free_str "mpfr_free_str" (char *str)

    int c_mpfr_const_pi "mpfr_const_pi" (mpfr_t rop, mpfr_rnd_t rnd)


# Make rounding mode values available to Python
MPFR_RNDN =  C_MPFR_RNDN
MPFR_RNDZ =  C_MPFR_RNDZ
MPFR_RNDU =  C_MPFR_RNDU
MPFR_RNDD =  C_MPFR_RNDD
MPFR_RNDA =  C_MPFR_RNDA
MPFR_RNDF =  C_MPFR_RNDF
MPFR_RNDNA =  C_MPFR_RNDNA


cdef class Mpfr:
    """ Mutable arbitrary-precision floating-point type. """
    cdef mpfr_t _value

    def __cinit__(self, precision):
        c_mpfr_init2(self._value, precision)

    def __dealloc__(self):
        c_mpfr_clear(self._value)


def mpfr_get_str(Mpfr op not None, int b = 10, mpfr_rnd_t rnd = MPFR_RNDN):
    """ Compute a base 'b' string representation for 'op'.

    'rnd' gives the rounding mode to use.

    Returns a pair (digits, exp) where:

        'digits' gives the string of digits
        exp is the exponent

    The exponent is normalized so that 0.<digits>E<exp> approximates 'op'.

    """
    cdef mpfr_exp_t exp
    cdef bytes digits

    c_digits = c_mpfr_get_str(NULL, &exp, 10, 0, op._value, rnd)
    if c_digits == NULL:
        raise RuntimeError("Error during string conversion.")

    try:
        digits = str(c_digits)
    finally:
        c_mpfr_free_str(c_digits)

    return digits, exp


def mpfr_const_pi(Mpfr rop not None, mpfr_rnd_t rnd):
    return c_mpfr_const_pi(rop._value, rnd)
