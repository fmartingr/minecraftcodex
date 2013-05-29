window.BlockRenderer = (model, textures, dom, width, height) ->
    # Globals
    _modelList = ['block']
    _renderer = null
    _scene = null
    _object = null
    _camera = null
    _cameraType = 'isometric'
    _lights = []

    # Set and check variables!
    _model = model
    if model not in _modelList
        return false

    # TODO CHECK TEXTURES!
    _textures = textures

    _domElement = document.querySelector dom
    if not _domElement
        return false

    _width = parseInt width
    _height = parseInt height

    if width == 'auto'
        _width = 'auto'
        _height = 'auto'
    else
        if not (_width > 0 and _height > 0)
            return false

    # Helpers
    # Checks for webgl support on the browser
    @checkWebGLsupport = ->
        return !!window.WebGLRenderingContext;

    @getWidth = ->
        return _domElement.clientWidth

    @setRendererSize = ->
        if _width == 'auto'
            width = @getWidth()
            height = width
        else
            width = _width
            height = _height
        _renderer.setSize width, height

        if _camera
            _camera.position.z = ( width / height ) * 40

    @setObjectScale = ->
        if _cameraType == 'isometric'
            scale = 7.5
            _object.scale.x = scale
            _object.scale.y = scale
            _object.scale.z = scale
        else
            scale = 0
            _object.scale.x = scale
            _object.scale.y = scale
            _object.scale.z = scale

    #
    #   WEBGL
    #

    @prepareCanvas = ->
        _renderer = new THREE.WebGLRenderer()
        @setRendererSize()
        #_renderer.domElement.id = 'webgl-canvas'
        _domElement.appendChild _renderer.domElement

    @prepareScene = ->
        _scene = new THREE.Scene()

    @prepareObject = ->
        _object = @models[_model].call()
        _object.overdraw = true
        _scene.add _object

    @prepareCamera = ->
        if _cameraType == 'isometric'
            _camera = new THREE.OrthographicCamera width / -2, width / 2, height / 2, height / -2, width * -2, width * 2
            _camera.lookAt _object.position
        else
            _camera = new THREE.PerspectiveCamera 45, width / height, 1, 1000
            _camera.position.z = ( width / height ) * 40


    @prepareLight = ->
        light = new THREE.DirectionalLight 0xffffff
        light.position.set(1, 20, 60).normalize()

        _scene.add light


    @animate = ->
        @setRendererSize()
        @setObjectScale()
        _renderer.render _scene, _camera

        requestAnimationFrame =>
            @animate()

    #
    #   MODELS
    #

    @models = 
        block: ->
            if not 'side' in _textures
                false
            else
                texture = new THREE.ImageUtils.loadTexture _textures['side']
                # We do not want blurry textures ;D
                texture.minFilter = THREE.NearestFilter
                texture.magFilter = THREE.NearestFilter

                material = new THREE.MeshLambertMaterial map: texture

                object = new THREE.Mesh new THREE.CubeGeometry(16, 16, 16), material
                object.rotation.set Math.PI/6, (Math.PI/4)*-1, 0
                
                object

    #
    #   INIT
    #

    @init = ->
        if @checkWebGLsupport()
            _domElement.style.width = "#{_width}px"
            _domElement.style.height = "#{_height}px"
            _domElement.innerHTML = ''
            @prepareCanvas()
            @prepareScene()
            @prepareObject()
            @prepareCamera()
            @prepareLight()
            @animate()


    @init()
