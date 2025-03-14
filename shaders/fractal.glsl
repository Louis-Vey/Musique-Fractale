#version 400

#if defined VERTEX_SHADER

in vec2 in_vert;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}

#elif defined FRAGMENT_SHADER

// Affiche l'ensemble de julia de la fractale sélectionné en juliaC
uniform bool julia;
uniform vec2 juliaC;

// Chaque fractales a son propre shader, créer avec un define différent pour chaque une.
// Les fichiers des fractales qui sont include en dessous doivent tous avoir une
// function appeler "compute" qui prend en paramètre les vec2 z, sqz(=z^2) et c
// et doivent renvoyer un vec2.
// Je conseil de marquer la compute comme inline.
// Ces fichiers doivent aussi définir le #define MAX_MAGNITUDE.
// Les points sont considérés dans la fractale quand |z| > MAX_MAGNITUDE.
// Ils peuvent aussi ajouter des variables uniform pour les utilisés dans compute.
// sqz est passé à la function avec il est utilisé pour calculé |z| et peut être réutiliser
// pour certaines function. Si la fractale ne l'utilise pas, le compiler devrait (au conditionnel)
// retirer tout seul l'argument.
#define MANDELBROT 0
#define NTHMANDELBROT 0
#define BURNINGSHIP 0
#if MANDELBROT == 1
#include "mandelbrot.glsl"

#elif NTHMANDELBROT == 1
#include "nthMandelbrot.glsl"

#elif BURNINGSHIP == 1
#include "burningShip.glsl"

#else
#error "Aucune fractale n'a été sélectionné"
#endif

#define SQ_MAX_MAGNITUDE (MAX_MAGNITUDE * MAX_MAGNITUDE)

uniform vec2 screenSize;
uniform vec2 center;
uniform vec2 zoom;
uniform int limit;

// Gradient de 16 couleur
uniform vec3 colorGradient[16];
// Active le dégradé de couleur (interpolation linéaire)
uniform bool smoothing;

out vec4 f_color;

void coloring(int i, vec2 z) {
    if (i == limit) {
        f_color = vec4(0, 0, 0, 1);
        return;
    }
    
    float smoothed;
    if (smoothing) {
        smoothed = log2(log2(float(sqrt(z.x*z.x + z.y*z.y))) / log2(2));
    }
    else smoothed = 0;
    float j = float(i) - smoothed;
    
    vec3 color = mix(colorGradient[int(floor(j)) % 16], colorGradient[int(floor(j) + 1) % 16], fract(j));
    f_color = vec4(color, 1);
}

void mainFractal() {
    vec2 c = (gl_FragCoord.xy / screenSize - 0.5) * zoom + center;
    vec2 z = c;
    vec2 sqz = vec2(z.x * z.x, z.y * z.y);

    int i = 0;
    while (i < limit && sqz.x + sqz.y < SQ_MAX_MAGNITUDE) {
        z = compute(z, sqz, c);
        sqz = vec2(z.x * z.x, z.y * z.y);
        i++;
    }

    coloring(i, z);
}

void juliaFractal() {
    vec2 z = (gl_FragCoord.xy / screenSize - 0.5) * zoom + center;
    vec2 sqz = vec2(z.x * z.x, z.y * z.y);

    int i = 0;
    while (i < limit && sqz.x + sqz.y < SQ_MAX_MAGNITUDE) {
        z = compute(z, sqz, juliaC);
        sqz = vec2(z.x * z.x, z.y * z.y);
        i++;
    }

    coloring(i, z);
}

void main() {
    if (julia) juliaFractal();
    else mainFractal();
}

#endif // FRAGMENT_SHADER