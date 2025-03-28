#ifndef CHIRIKOV_INCLUDE
#define CHIRIKOV_INCLUDE

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // zx = zy
    // zx = -cy*zx + cx*zy - zy³
    return vec2(
        z.y,
        -c.y*z.x + c.x*z.y - z.y*z.y*z.y
    );
}

bool inside(vec2 z, vec2 sqz) {
    return sqz.x + sqz.y < 100;
}

#endif