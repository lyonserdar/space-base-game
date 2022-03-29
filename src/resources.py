import pyglet

from .tile import TileType

pyglet.resource.path = ["assets", "assets/tiles"]
pyglet.resource.reindex()

# For pixel art removes the default smooth filtering
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

tiles = {
    TileType.EMPTY: None,
    TileType.FLOOR: pyglet.resource.image("tiles/floor.png"),
}

tile_highlighter = pyglet.resource.image("highlight.png")
