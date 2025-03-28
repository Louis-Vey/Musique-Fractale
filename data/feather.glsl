#ifndef FEATHER_INCLUDE
#define FEATHER_INCLUDE

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // z = z³ / (z²+1) + c

    // (a+bi)³ = a³ + 3a²bi + 3ab²i² + b³i³
    // (a+bi)³ = a³ + 3a²bi - 3ab² - b³i
    // (a+bi)³ = a³ - 3ab² + 3a²bi - b³i
    vec2 cbz = vec2(
        z.x*z.x*z.x - 3*z.x*z.y*z.y,
        3*z.x*z.x*z.y - z.y*z.y*z.y
    );

    vec2 sqz1 = vec2(sqz.x+1, sqz.y);

    // (a+bi)/(c+di) = (ac+bd) / (c²+d²) + i(bc-ad) / (c²+d²)
    vec2 top = vec2(cbz.x*sqz1.x + cbz.y*sqz1.y, cbz.y*sqz1.x - cbz.x*sqz1.y);
    float bottom = sqz1.x*sqz1.x + sqz1.y*sqz1.y;

    vec2 q = top / bottom;
    return vec2(q.x + c.x, q.y + c.y);
}

bool inside(vec2 z, vec2 sqz) {
    return sqz.x + sqz.y < 1000;
}

#endif