#version 330 core

uniform sampler2D uiTex;

//uniform float time;
uniform vec3 backgroundColor;
uniform vec2 resolution;

//uniform vec2 resolution;
//uniform vec2 cameraPos;
//uniform float cameraDist;

in vec2 uvs;
out vec4 color;

const int samples = 15,
            LOD = 2,
            sLOD = 1 << LOD;
const float sigma = float(samples) * .25;

float gaussian(vec2 i) {
    return exp( -.5* dot(i/=sigma,i) ) / ( 6.28 * sigma*sigma );
}

vec4 blur(sampler2D sp, vec2 U, vec2 scale) {
    vec4 O = vec4(0);
    int s = samples/sLOD;

    for ( int i = 0; i < s*s; i++ ) {
        vec2 d = vec2(i%s, i/s)*float(sLOD) - float(samples)/2.;
        O += gaussian(d) * textureLod( sp, U + scale * d , float(LOD) );
    }

    return O / O.a;
}

void main() {
    // Getting colors from textures
    vec4 color1 = texture(uiTex, uvs);
    color1 = blur(uiTex, uvs, 1./resolution);
    //vec4 color2 = texture(uiTex, uvs);

    // Layering textures with alpha blending
    //color = mix(color1, color2, color2.a);
    // if we have next texture ex. color3, we can layer it like this:
    // color = mix(color, color3, color3.a);

    // Adding background color
    color = mix(color1, vec4(backgroundColor, 1.0), 1.0 - color1.a);
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