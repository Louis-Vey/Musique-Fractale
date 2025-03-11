#ifndef COLORING
#define COLORING

vec3 coloring(int i, int limit, vec3[16] colorGradient, bool smoothing, dvec2 z) {
    if (i == limit) return vec3(0, 0, 0);
    
    float smoothed;
    if (smoothing) {
        // https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set#Continuous_(smooth)_coloring
        smoothed = log2(log2(float(sqrt(z.x*z.x + z.y*z.y))) / log2(2));
    }
    else smoothed = 0;
    float j = float(i) - smoothed;
    return mix(colorGradient[int(floor(j)) % 16], colorGradient[int(floor(j) + 1) % 16], fract(j));
}

#endif