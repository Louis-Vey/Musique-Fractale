#version 330

#if defined VERTEX_SHADER

in vec2 in_pos;
in vec2 in_c;
uniform uint limit;

flat out uint iteration;

void main() {
    vec2 z = in_c;
    uint i = 0u;
    while (i < limit && z[0] * z[0] + z[1] * z[1] < 4) {
        z = vec2(z[0] * z[0] - z[1] * z[1], 2 * z[0] * z[1]);
        i++;
    }
    gl_Position = vec4(in_pos, 0.0, 1.0);
    iteration = i;
}

#elif defined FRAGMENT_SHADER

flat in uint iteration;
uniform uint limit;

out vec3 f_color;

void main() {
    if (iteration == limit) {
        f_color = vec3(1, 1, 1);
    } else {
        f_color = vec3(0, 0, 0);
    }
}

#endif