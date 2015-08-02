#version 430

layout (location = 13) uniform mat4 modelMatrix;
layout (location = 17) uniform mat4 viewMatrix;
layout (location = 21) uniform mat4 normalMatrix;
layout (location = 25) uniform mat4 projectionMatrix;

layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 nor;
layout (location = 2) in vec2 tex;
layout (location = 3) in vec3 tan;
layout (location = 4) in mat4 inst_model_matrix;
layout (location = 8) in mat4 inst_normal_matrix;
layout (location = 12) uniform int useInstancing;

out VertexData
{
	vec3 position;
	vec3 normal;
	vec3 tangent;
	vec2 texcoord;
} VertexOut;

void main()
{
    if (useInstancing > 0) {
        vec4 world_pos = inst_model_matrix * vec4(pos.xyz, 1);
        gl_Position = projectionMatrix * viewMatrix * world_pos;
        VertexOut.position = vec3(viewMatrix * world_pos);
        VertexOut.normal = vec3(inst_normal_matrix * vec4(nor.xyz, 1.0));
        VertexOut.tangent = vec3(viewMatrix * inst_model_matrix * vec4(tan.xyz, 1.0));
        VertexOut.texcoord = vec2(tex.xy);
    } else {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos.xyz, 1);
        VertexOut.position = vec3(viewMatrix * modelMatrix * vec4(pos.xyz,1));
        VertexOut.normal = vec3(normalMatrix * vec4(nor.xyz,1));
        VertexOut.tangent = vec3(viewMatrix * modelMatrix * vec4(tan.xyz, 0.0));
        VertexOut.texcoord = vec2(tex.xy);
    }
}
