#version 400

#include "coloring.frag"

uniform vec2 screenSize;
uniform vec2 center;
uniform vec2 zoom;
uniform int limit;
uniform vec2 c;

uniform vec3 colorGradient[16];

out vec3 f_color;

void main() {
    vec2 z = (gl_FragCoord.xy / screenSize - 0.5) * zoom + center;
    vec2 sqz = vec2(z.x * z.x, z.y * z.y);
    int i = 0;
    while (i < limit && sqz.x + sqz.y < 4) {
        // (a+bi)^2 = a^2 - b^2 + 2abi
        z = vec2(sqz.x - sqz.y, (z.x + z.x) * z.y) + c;
        sqz = vec2(z.x * z.x, z.y * z.y);
        i++;
    }

    f_color = coloring(i, limit, colorGradient, true, dvec2(z));
}