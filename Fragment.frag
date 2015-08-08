#version 430

layout (location = 29) uniform sampler2D textureSampler;
layout (location = 30) uniform int useTexture;
layout (location = 31) uniform vec4 color;
layout (location = 32) uniform int useLighting;

in VertexData
{
    vec3 position;
    vec3 normal;
    vec2 texcoord;
} VertexIn;

out vec4 fragColor;

void main()
{
    fragColor = color;
    if (useTexture > 0) {
        fragColor *= texture(textureSampler, VertexIn.texcoord.xy);
    }
    float alpha = fragColor.a;
    if (useLighting > 0) {
        fragColor *= max(dot(normalize(VertexIn.normal), vec3(0, 0, 1)), 0.1);
    }
    float fog = clamp(0.002 * sqrt(dot(VertexIn.position, VertexIn.position)) - 100.0, 0, 1);
    fragColor.a = (1 - fog) * alpha;
}
