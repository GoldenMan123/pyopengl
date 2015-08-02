#version 430

layout (location = 29) uniform sampler2D textureSampler;
layout (location = 30) uniform int useTexture;
layout (location = 31) uniform vec4 color;

in VertexData
{
	vec3 position;
	vec3 normal;
	vec3 tangent;
	vec2 texcoord;
} VertexIn;

out vec4 fragColor;

void main()
{
    fragColor = color;
    if (useTexture > 0) {
        fragColor *= texture(textureSampler, VertexIn.texcoord.xy);
	}
	if (fragColor.a < 0.1) {
        discard;
	}
}