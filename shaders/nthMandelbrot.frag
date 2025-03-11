#version 400

#include "coloring.frag"

uniform vec2 screenSize;
uniform vec2 center;
uniform vec2 zoom;
uniform int limit;
uniform float power;

uniform vec3 colorGradient[16];

out vec3 f_color;

void main() {
    float halvedPower = power / 2;
    vec2 c = (gl_FragCoord.xy / screenSize.xy - 0.5) * zoom + center;
    vec2 z = c;
    vec2 sqz = vec2(z.x * z.x, z.y * z.y);
    int i = 0;
    while (i < limit && sqz.x + sqz.y < 4) {
        // (a+bi)^n = r^n(cos(n * angle) + isin(n * angle))
        // r = sqrt(a^2 + b^2), angle = arctan(b / a)
        float delta = power * atan(z.y, z.x);
        float rn = pow(sqz.x + sqz.y, halvedPower); // sqrt(x)^n = x^(n/2)

        z = rn * vec2(cos(delta), sin(delta)) + c;
        sqz = vec2(z.x * z.x, z.y * z.y);
        i++;
    }

    f_color = coloring(i, limit, colorGradient, true, z);
}