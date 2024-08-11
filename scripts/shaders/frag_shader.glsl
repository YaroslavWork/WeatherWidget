#version 330 core

uniform sampler2D backgroundTex;
uniform sampler2D uiTex;
uniform sampler2D buttonsTex;
uniform sampler2D shadowTex;

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

    for ( int i = 0; i < s*s; i++ ) {
        vec2 d = vec2(i%s, i/s)*float(sLOD) - float(samples)/2.;
        if ( U.x < 0.02 || U.x > 0.98 || U.y < 0.05 || U.y > 0.95 ) {
            // Just copy the pixel if it's on the edge
            O += textureLod( sp, U, float(LOD) );
        }
        else {
            O += gaussian(d) * textureLod( sp, U + scale * d , float(LOD) );
        }

    }

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


void main() {
    // Getting colors from textures
    vec4 color1 = blur(backgroundTex, uvs, 1./resolution, 15, 1);
    vec4 color2 = texture(uiTex, uvs);
    vec4 color3 = mouseDist(buttonsTex, uvs, mousePos);
    float weights[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);
    vec4 color4 = texture(shadowTex, uvs) * weights[0];

    for (int i = 1; i < 5; ++i) {
        color4 += texture(shadowTex, uvs + vec2(0.0, 0.003 * i)) * weights[i];
        color4 += texture(shadowTex, uvs + vec2(0.0, -0.003 * i)) * weights[i];
        color4 += texture(shadowTex, uvs + vec2(0.003 * i, 0.0)) * weights[i];
        color4 += texture(shadowTex, uvs + vec2(-0.003 * i, 0.0)) * weights[i];
    }
    color4.a = 0.35 * color4.a;

    // Layering textures with alpha blending
    color = mix(color1, color4, color4.a);
    // if we have next texture ex. color3, we can layer it like this:
    color = mix(color, color2, color2.a);
    color = mix(color, color3, color3.a);

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