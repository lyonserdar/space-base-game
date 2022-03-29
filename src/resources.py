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

# TODO: change the location of walls
wall_spritesheet = pyglet.resource.image("tiles/walls.png")
wall_seq = pyglet.image.ImageGrid(wall_spritesheet, 6, 9)
walls = {0: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 6]}


tile_highlighter = pyglet.resource.image("highlight.png")
