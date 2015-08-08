#version 430

layout (location = 13) uniform mat4 modelMatrix;
layout (location = 17) uniform mat4 viewMatrix;
layout (location = 21) uniform mat4 normalMatrix;
layout (location = 25) uniform mat4 projectionMatrix;

layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 nor;
layout (location = 2) in vec2 tex;

out VertexData
{
	vec3 position;
	vec3 normal;
	vec2 texcoord;
} VertexOut;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos.xyz, 1);
    VertexOut.position = vec3(viewMatrix * modelMatrix * vec4(pos.xyz,1));
    VertexOut.normal = vec3(normalMatrix * vec4(nor.xyz,1));
    VertexOut.texcoord = vec2(tex.xy);
}
