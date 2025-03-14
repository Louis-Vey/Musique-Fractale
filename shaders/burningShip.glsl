#ifndef BURNING_SHIP_INCLUDE
#define BURNING_SHIP_INCLUDE

#define MAX_MAGNITUDE 2

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // (|a|+|b|i)^2 = |a|^2 - |b|^2 + |2ab|i
    //              = a^2 - b^2 + |2ab|i
    //              = a^2 - b^2 + |(a+a)b|i
    return vec2(sqz.x - sqz.y, abs((z.x + z.x) * z.y)) + c;
}

#endif