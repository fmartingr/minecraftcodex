#
#   CAMERAS
#
class Camera
    _near: 1
    _far: 1000

    _position:
        x: 0
        y: 0
        z: 0

    move: (x, y, z) ->
        @_position.x += x
        @_position.y += y
        @_position.z += z
        @_self.position = @_position
        $('input.camera-x').val @_position.x
        $('input.camera-y').val @_position.y
        $('input.camera-z').val @_position.z

    goTo: (x, y, z) ->
        @_position.x = x
        @_position.y = y
        @_position.z = z
        @_self.position = @_position
        $('input.camera-x').val @_position.x
        $('input.camera-y').val @_position.y
        $('input.camera-z').val @_position.z

class orthograpicCamera extends Camera
    _self: null
    _left: 0
    _right: 0
    _top: 0
    _bottom: 0

    _near: -1000
    _far: 1000

    init: (width, height) ->
        @_left = width / -2
        @_right = width / 2
        @_top = height / 2
        @_bottom = height / -2
        @_near = width * -2
        @_far = width * 2
        camera = new THREE.OrthographicCamera @_left, @_right, @_top, @_bottom, @_near, @_far
        @_self = camera
        @goTo 0, 0, 0


class perspectiveCamera extends Camera
    _fov: 45
    _aspectRatio: 0
    _near: 1
    _far: 1000

    init: (width, height) ->
        @_aspectRatio = width / height
        camera = new THREE.PerspectiveCamera @_fov, @_aspectRatio, @_near, @_far
        @_self = camera
        @goTo 0, 0, 40


window.StudioCameras =
    orthographicCamera: orthograpicCamera
    perspectiveCamera: perspectiveCamera
