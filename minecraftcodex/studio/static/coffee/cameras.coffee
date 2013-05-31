#
#   CAMERAS
#
orthograpicCamera = 
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


perspectiveCamera = 
    _fov: 45
    _aspectRatio: 0
    _near: 1
    _far: 1000

    init: (width, height) ->
        @_aspectRatio = width / height
        camera = new THREE.PerspectiveCamera @_fov, @_aspectRatio, @_near, @_far
        camera.position.z = 40
        @_self = camera


window.StudioCameras =
    orthographicCamera: orthograpicCamera
    perspectiveCamera: perspectiveCamera
