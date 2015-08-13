'''
Scene for test objectcube, perpective projection,
translation, rotation, scaling matrices,
texturing, lighting and camera
'''

import sys
sys.path.insert(0, '.')

if __name__ == '__main__':
    import glfw
    import time
    from engine import *
    from gui import *
    from glutils import *
    from objectcube import *
    import OpenGL.GL as gl

    # Initialize the library
    if not glfw.init():
        sys.exit()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Scene 2", None, None)
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
        engine.setWindowHeight(height)
        engine.setWindowWidth(width)
        pass

    # Install a window size handler
    glfw.set_window_size_callback(window, on_resize)

    def on_mouse(window, button, action, mods):
        pass

    glfw.set_mouse_button_callback(window, on_mouse)

    old_time = time.time()
    elapsed_time = 0.0
    runtime = 0.0

    # Create engine, gui and cube object
    engine = Engine(window)
    engine.setWindowHeight(height)
    engine.setWindowWidth(width)
    gui = GUI()
    gui.setWindowHeight(height)
    gui.setWindowWidth(width)
    cube = objectCube()
    glfw.set_cursor_pos(window, width / 2, height / 2)

    #Init texture
    gui.initTexture(0, "tests/data/mmp_gurov.png")
    gui.bindTexture(0)

    # Render function
    def render():
        # Clear screen
        gl.glClearColor(0.25 * (1 - cos(0.5 * runtime)), 0.5 * (1 + sin(1 * runtime)),
            0.5 * (1 + cos(0.33 * runtime)), 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glViewport(0, 0, gui.window_width, gui.window_height)
        # Draw scene
        engine._Engine__process_camera()
        gui.enableLighting()
        gui.projectionMatrix = gui.perspective()
        gui.eye = array([0, 2, -10], 'f')
        gui.cen = gui.eye + engine.cam_dir
        gui.up  = engine.cam_up
        gui.viewMatrix = gui.lookAt()
        gui.modelMatrix = mul(mul(translate(array([0, 0, 0.5 * sin(2 * runtime)], 'f')),
            rotate(runtime * 100, array([0, 1, 0], 'f'))), scale(array([0.5, 0.5, 0.5], 'f')))
        gui.sendMatrices()
        gui.setColor(array([1, 1, 0, 1], 'f'))
        cube.draw()
        gui.modelMatrix = mul(translate(array([0, 0, -0.5 * sin(2 * runtime)], 'f')),
            rotate(-runtime * 200, array([0, 1, 0], 'f')))
        gui.sendMatrices()
        gui.setColor(array([0, 1, 1, 1], 'f'))
        cube.draw()
        for i in range(8):
            gui.modelMatrix = mul(rotate(-runtime * 50 + 360.0 * i / 8, array([0, 1, 0], 'f')),
                translate(array([0, 0, 3 + sin(runtime)], 'f')))
            gui.sendMatrices()
            gui.setColor(array([0.25, 1 - 0.5 * (1 + sin(runtime)), 0.5 * (1 + sin(runtime)), 1], 'f'))
            cube.draw()

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Calculate elapsed time
        elapsed_time = time.time() - old_time
        old_time = time.time()
        runtime += elapsed_time

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
