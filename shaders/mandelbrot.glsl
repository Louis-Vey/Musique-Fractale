#ifndef MANDELBROT_INCLUDE
#define MANDELBROT_INCLUDE

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // (a+bi)^2 = a^2 - b^2 + 2abi
    //          = a^2 - b^2 + (a+a)bi
    return vec2(sqz.x - sqz.y, (z.x + z.x) * z.y) + c;
}

bool inside(vec2 z, vec2 sqz) {
    return sqz.x + sqz.y < 4;
}

#endif