class Entity
    _object: null

    _id: null

    _visible: true

    _position:
        x: 0
        y: 0
        z: 0

    _rotation:
        x: 0
        y: 0
        z: 0

    _scale:
        x: 0
        y: 0
        z: 0

class Cube extends Entity
    name: 'Cube'

    init: (size) ->
        @_shape = new THREE.CubeGeometry size.x, size.y, size.z
        @_texture = new THREE.MeshNormalMaterial

        @_object = new THREE.Mesh @_shape, @_texture
        @

class Sphere extends Entity
    name: 'Sphere'

    init: (size) ->
        @_shape = new THREE.SphereGeometry size.x, size.y, size.z
        @_texture = new THREE.MeshNormalMaterial

        @_object = new THREE.Mesh @_shape, @_texture
        @


window.StudioObjects = 
    cube: Cube
    sphere: Sphere
