'''
Scene for test text rendering
'''

import sys
sys.path.insert(0, '.')

if __name__ == '__main__':
    import glfw
    import time
    from gui import *
    from glutils import *
    from objectquad import *
    import OpenGL.GL as gl

    # Initialize the library
    if not glfw.init():
        sys.exit()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(500, 500, "Scene 3", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Make the window's context current
    glfw.make_context_current(window)

    # Get window size
    width, height = glfw.get_framebuffer_size(window)

    def on_resize(window, width, height):
        gui.setWindowHeight(height)
        gui.setWindowWidth(width)
        pass

    # Install a window size handler
    glfw.set_window_size_callback(window, on_resize)

    def on_mouse(window, button, action, mods):
        pass

    glfw.set_mouse_button_callback(window, on_mouse)

    old_time = time.time()
    elapsed_time = 0.0

    # Create gui and quad object
    gui = GUI()
    gui.setWindowHeight(height)
    gui.setWindowWidth(width)
    quad = objectQuad()
    gui.renderText(0, "data/mono.ttf", 256, "RED", (255, 255, 255, 255))
    gui.renderText(1, "data/mono.ttf", 256, "GREEN", (255, 255, 255, 255))
    gui.renderText(2, "data/mono.ttf", 256, "BLUE", (255, 255, 255, 255))

    # Render function
    def render():
        # Clear screen
        gl.glClearColor(0, 0, 0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glViewport(0, 0, gui.window_width, gui.window_height)
        # Draw
        gui.projectionMatrix = identity(4, 'f')
        gui.viewMatrix = identity(4, 'f')
        gui.bindTexture(0)
        gui.modelMatrix = mul(translate(array([0, 0.5, 0], 'f')),
            scale(array([1, 0.5, 1], 'f')))
        gui.sendMatrices()
        gui.setColor(array([1, 0, 0, 1], 'f'))
        quad.draw()
        gui.bindTexture(1)
        gui.modelMatrix = mul(translate(array([0, 0.0, 0], 'f')),
            scale(array([1.5, 0.5, 1], 'f')))
        gui.sendMatrices()
        gui.setColor(array([0, 1, 0, 1], 'f'))
        quad.draw()
        gui.bindTexture(2)
        gui.modelMatrix = mul(translate(array([0, -0.5, 0], 'f')),
            scale(array([1, 0.5, 1], 'f')))
        gui.sendMatrices()
        gui.setColor(array([0, 0, 1, 1], 'f'))
        quad.draw()

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Calculate elapsed time
        elapsed_time = time.time() - old_time
        old_time = time.time()

        # Render scene
        render()

        # Swap front and back buffers
        glfw.swap_interval(1)
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

        # Don't be egoist :)
        time.sleep(0.01)

    glfw.terminate()
