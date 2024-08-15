#version 330 core

uniform sampler2D backgroundTex;
uniform sampler2D uiTex;
uniform sampler2D buttonsTex;
uniform sampler2D shadowTex;
uniform sampler2D appShadowTex;

//uniform float time;
uniform vec3 backgroundColor;
uniform vec2 resolution;
uniform vec2 mousePos;
uniform float mouseOutsideTime;

//uniform vec2 resolution;
//uniform vec2 cameraPos;
//uniform float cameraDist;

in vec2 uvs;
out vec4 color;

const int samples = 15,
            LOD = 1,
            sLOD = 1 << LOD;
const float sigma = float(samples) * .25;

float gaussian(vec2 i) {
    return exp( -.5* dot(i/=sigma,i) ) / ( 6.28 * sigma*sigma );
}

vec4 blur(sampler2D sp, vec2 U, vec2 scale, int samples, int LOD) {
    int sLOD = 1 << LOD;
    vec4 O = vec4(0);
    int s = samples/sLOD;

    // Define the rounded rectangle parameters
    vec2 rectSize = vec2(0.96, 0.90);  // Size of the rectangle (width, height)
    vec2 rectPos = vec2(0.02, 0.05);   // Position of the bottom-left corner
    float radius = 0.;               // Radius of the rounded corners

    // Calculate the distance to the edges, considering the rounded corners
    vec2 cornerDist = abs(U - (rectPos + rectSize * 0.5)) - (rectSize * 0.5 - vec2(radius));

    // Determine if the pixel is inside the rounded rectangle
    float inside = step(max(cornerDist.x, cornerDist.y), 0.0) + step(length(max(cornerDist, 0.0)), radius);

    for ( int i = 0; i < s*s; i++ ) {
        vec2 d = vec2(i%s, i/s)*float(sLOD) - float(samples)/2.;
        if (inside < 1.0) {
            // Just copy the pixel if it's on the edge
            return textureLod( sp, U, float(LOD) );
        }
        else {
            O += gaussian(d) * textureLod( sp, U + scale * d , float(LOD) );
        }

    }

    // Mixing pixel with 5% of gray color
    O = mix(O, vec4(.5), 0.05);

    return O / O.a;
}

vec4 mouseDist(sampler2D sp, vec2 U, vec2 mousePos) {
    float mouseOutsideTime = clamp(mouseOutsideTime, 1., 100.);
    // Distance between mouse and pixel
    float dist = 1.-length(U - mousePos)*1.5*(mouseOutsideTime*mouseOutsideTime);
    // Make a dist between 0 and 1
    dist = clamp(dist, 0., 0.75);
    // Combine texture with transparency
    if (texture(sp, U).a < 0.1) {
        return vec4(0.0, 0.0, 0.0, 0.0);
    }

    return vec4(texture(sp, U).rgb, dist);
}

vec4 blur2(sampler2D sp, vec2 U, float offset, int steps) {
    float weights[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);
    vec4 result = vec4(0.0);

    for (int i = 0; i < steps; ++i) {
        result += texture(sp, U + vec2(0.0, offset * i)) * weights[i];
        result += texture(sp, U + vec2(0.0, -offset * i)) * weights[i];
        result += texture(sp, U + vec2(offset * i, 0.0)) * weights[i];
        result += texture(sp, U + vec2(-offset * i, 0.0)) * weights[i];
    }

    return result;
}


void main() {
    // Getting colors from textures
    vec4 color1 = blur(backgroundTex, uvs, 1./resolution, 15, 1);
    vec4 color2 = texture(uiTex, uvs);
    vec4 color3 = mouseDist(buttonsTex, uvs, mousePos);

    vec4 color4 = blur2(shadowTex, uvs, 0.006, 5);
    color4.a = 0.25 * color4.a;
    vec4 color5 = texture(appShadowTex, uvs);
    color5.a = 0.05 * color5.a;

    // Layering textures with alpha blending
    color = mix(color1, color4, color4.a);
    // if we have next texture ex. color3, we can layer it like this:
    color = mix(color, color2, color2.a);
    color = mix(color, color3, color3.a);
    color = mix(color, color5, color5.a);

    // Adding background color
    color = mix(color, vec4(backgroundColor, 1.0), 1.0 - color1.a);
}


// ----- Find a local point in the camera space -----
/*
    // Make uvs as x and y scaled one by one
    vec2 uv = uvs;
    float scale;
    if (resolution.x < resolution.y) {
        scale = resolution.x / resolution.y;
        uv.x = uvs.x * scale;
    } else {
        scale = resolution.y / resolution.x;
        uv.y = uvs.y * scale;
    }

    // Make a rectangle from x=100 to x=200 and y=100 to y=200
    vec2 point = vec2(uv.x * cameraDist + cameraPos.x, uv.y * cameraDist + cameraPos.y);
*/