#ifndef SIN_INCLUDE
#define SIN_INCLUDE

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // z = sin(z)*c
    // (a+bi) = sin(a)cosh(b) + cos(a)sinh(b)i
    vec2 s = vec2(
        sin(z.x) * cosh(z.y),
        cos(z.x) * sinh(z.y)
    );

    // (a+bi)(c+di) = ac - bd + bci + adi
    return vec2(
        s.x*c.x - s.y*c.y,
        s.x*c.y + s.y*c.x
    );
}

bool inside(vec2 z, vec2 sqz) {
    return abs(z.y) <= 50;
}

#endif