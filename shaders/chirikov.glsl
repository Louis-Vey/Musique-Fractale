#ifndef CHIRIKOV_INCLUDE
#define CHIRIKOV_INCLUDE

vec2 compute(vec2 z, vec2 sqz, vec2 c) {
    // zy = zy + cy * sin(zx)
    // zx = zx + cx * (zy + cy * sin(zx))
    float zy = z.y + c.y*sin(z.x);
    float zx = z.x + c.x*zy;

    return vec2(zx, zy);
}

bool inside(vec2 z, vec2 sqz) {
    return sqz.x + sqz.y < 10000;
}

#endif