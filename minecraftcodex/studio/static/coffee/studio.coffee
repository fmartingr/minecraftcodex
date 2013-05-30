Studio =
    domElement: null

    renderer: null
    width: 600
    height: 600

    scene: null

    camera: null

    animating: false

    lights: []
    _lights: {}
    
    objects: []
    _objects: {}
    
    # Methods
    checkWebGLsupport: ->
        return !!window.WebGLRenderingContext;

    # ChangeCamera
    onCameraChange: (cameraType) ->
        if "#{cameraType}Camera" of StudioObjects
            @camera = StudioObjects["#{cameraType}Camera"].init @width, @height
            if not @animating
                @animate()

    # Animation
    animate: ->
        if @scene and @camera
            @renderer.render @scene, @camera

            requestAnimationFrame =>
                @animate()

    setSize: (width, height) ->
        @width = parseInt width
        @height = parseInt height

        @renderer.setSize @width, @height
        @domElement.style.width = "#{@width}px"
        @domElement.style.height = "#{@height}px"

    init: (dom, width, height) ->
        if not @checkWebGLsupport()
            return false

        @domElement = document.querySelector dom

        @renderer = new THREE.WebGLRenderer()
        @setSize width, height

        @domElement.appendChild @renderer.domElement

        @scene = new THREE.Scene()

        # test
        @object = new THREE.Mesh new THREE.CubeGeometry(16, 16, 16), new THREE.MeshNormalMaterial()

        @scene.add @object
        # /test

        @animate()

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


window.Studio = Studio
window.StudioObjects =
    'orthographicCamera': orthograpicCamera
    'perspectiveCamera': perspectiveCamera
