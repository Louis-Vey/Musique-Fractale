#ifndef NTH_MANDELBROT_INCLUDE
#define NTH_MANDELBROT_INCLUDE

#define MAX_MAGNITUDE 2

uniform float power;
uniform float halvedPower;

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // (a+bi)^n = r^n(cos(n * angle) + isin(n * angle))
    // r = sqrt(a^2 + b^2), angle = arctan(b / a)
    float delta = power * atan(z.y, z.x);
    float rn = pow(sqz.x + sqz.y, halvedPower); // sqrt(x)^n = x^(n/2)

    return rn * vec2(cos(delta), sin(delta)) + c;
}

#endif