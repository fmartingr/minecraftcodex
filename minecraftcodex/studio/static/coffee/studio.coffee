Studio =
    domElement: null

    renderer: null
    width: 600
    height: 600

    scene: null

    camera: null

    lights: []
    _lights: {}
    
    objects: []
    _objects: {}
    
    # Methods
    checkWebGLsupport: ->
        return !!window.WebGLRenderingContext;

    init: (dom, width, height) ->
        if not @checkWebGLsupport()
            return false

        @domElement = document.querySelector dom

        @renderer = new THREE.WebGLRenderer()
        @renderer.setSize width, height

        @domElement.appendChild @renderer.domElement


window.Studio = Studio
