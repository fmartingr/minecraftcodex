Studio =
    domElement: null
    _dom: null

    renderer: null
    width: 600
    height: 600

    scene: null

    camera: null
    _cameraType: null

    animating: false

    lights: []
    _lights: {}
    
    objects: []
    _objects: {}
    
    # Methods
    checkWebGLsupport: ->
        return !!window.WebGLRenderingContext;

    # Callbacks
    onCameraChange: (cameraType) ->
        if "#{cameraType}Camera" of StudioObjects
            @_cameraType = cameraType
            @camera = StudioObjects["#{cameraType}Camera"].init @width, @height
            if not @animating
                @animate()

    # Animation
    animate: ->
        if @scene and @camera
            if not @animating
                @animating = true
            @renderer.render @scene, @camera

            @_animationFrame = requestAnimationFrame =>
                @animate()

    # Scene helpers
    setSize: (width, height) ->
        @width = parseInt width
        @height = parseInt height

        @renderer.setSize @width, @height
        @domElement.style.width = "#{@width}px"
        @domElement.style.height = "#{@height}px"

        @onCameraChange @_cameraType

    # Tests
    changeTexture: (path) ->
        @scene.remove @object

        texture = new THREE.ImageUtils.loadTexture path
        texture.minFilter = THREE.NearestFilter
        texture.magFilter = THREE.NearestFilter
        material = new THREE.MeshLambertMaterial map: texture
        @object = new THREE.Mesh new THREE.CubeGeometry(16, 16, 16), material
        @object.rotation.set Math.PI/6, (Math.PI/4)*-1, 0
        @scene.add @object

    reset: ->
        cancelAnimationFrame @_animationFrame
        @renderer.domElement.remove()
        @init @_dom, @width, @height

    init: (dom, width, height) ->
        if not @checkWebGLsupport()
            return false

        @domElement = document.querySelector dom
        @_dom = dom

        @renderer = new THREE.WebGLRenderer()
        @setSize width, height

        @domElement.appendChild @renderer.domElement

        @scene = new THREE.Scene()

        # test
        @light = new THREE.DirectionalLight 0xffffff
        @light.position.set(1, 20, 60).normalize()
        @light.intensity = 1.6
        @scene.add @light

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
