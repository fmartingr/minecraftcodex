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
        if "#{cameraType}Camera" of window.StudioCameras
            @_cameraType = cameraType
            @camera = window.StudioCameras["#{cameraType}Camera"].init @width, @height
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

        #@object = new THREE.Mesh new THREE.CubeGeometry(16, 16, 16), new THREE.MeshNormalMaterial()

        #@scene.add @object
        # /test

        @animate()


window.Studio = Studio
