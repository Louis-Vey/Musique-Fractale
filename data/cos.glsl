#ifndef COS_INCLUDE
#define COS_INCLUDE

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // z = cos(z)*c
    // (a+bi) = cos(a)cosh(b) + sin(a)sinh(b)i
    vec2 s = vec2(
        cos(z.x) * cosh(z.y),
        sin(z.x) * sinh(z.y)
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