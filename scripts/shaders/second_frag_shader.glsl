#version 330 core

uniform sampler2D uiTex;

in vec2 uvs;
out vec4 color;

float smoothTransition(float value) {
    // Smooth transition from 0 to 1 between 0.15 and 0.3
    float lowerTransition = smoothstep(0.15, 0.3, value);

    // Smooth transition from 1 to 0 between 0.7 and 0.85
    float upperTransition = smoothstep(0.85, 0.7, value);

    // Combine the two transitions
    return lowerTransition * upperTransition;
}

void main()
{
    vec4 texColor = texture(uiTex, uvs);
    // Using transition as a alpha value
    color = vec4(texColor.rgb, smoothTransition(texColor.a));
}