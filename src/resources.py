import pyglet

from .tile import TileType

pyglet.resource.path = ["resources", "resources/tiles", "resources/audio"]
pyglet.resource.reindex()

# For pixel art removes the default smooth filtering
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

tiles = {
    TileType.EMPTY: None,
    TileType.FLOOR: pyglet.resource.image("tiles/floor.png"),
}

wall_spritesheet = pyglet.resource.image("tiles/walls.png")
wall_seq = pyglet.image.ImageGrid(wall_spritesheet, 6, 9)

structures = {
    "wall": {
        0: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 6],
        1: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 5],
        2: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 6],
        3: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 1],
        4: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 6],
        5: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 2],
        6: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 0],
        7: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 4],
        8: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 5],
        9: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 1],
        10: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 2],
        11: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 4],
        12: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 0],
        13: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 3],
        14: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 3],
        15: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 7],
        19: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 8],
        23: pyglet.image.TextureGrid(wall_seq)[9 * 0 + 5],
        27: pyglet.image.TextureGrid(wall_seq)[9 * 0 + 3],
        31: pyglet.image.TextureGrid(wall_seq)[9 * 0 + 1],
        38: pyglet.image.TextureGrid(wall_seq)[9 * 4 + 7],
        39: pyglet.image.TextureGrid(wall_seq)[9 * 0 + 4],
        46: pyglet.image.TextureGrid(wall_seq)[9 * 0 + 2],
        47: pyglet.image.TextureGrid(wall_seq)[9 * 0 + 0],
        55: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 5],
        63: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 2],
        76: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 7],
        77: pyglet.image.TextureGrid(wall_seq)[9 * 1 + 4],
        78: pyglet.image.TextureGrid(wall_seq)[9 * 1 + 2],
        79: pyglet.image.TextureGrid(wall_seq)[9 * 1 + 0],
        95: pyglet.image.TextureGrid(wall_seq)[9 * 1 + 6],
        110: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 4],
        111: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 3],
        127: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 1],
        137: pyglet.image.TextureGrid(wall_seq)[9 * 5 + 8],
        139: pyglet.image.TextureGrid(wall_seq)[9 * 1 + 3],
        141: pyglet.image.TextureGrid(wall_seq)[9 * 1 + 5],
        143: pyglet.image.TextureGrid(wall_seq)[9 * 1 + 1],
        155: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 5],
        159: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 2],
        175: pyglet.image.TextureGrid(wall_seq)[9 * 0 + 6],
        191: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 0],
        205: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 4],
        207: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 3],
        223: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 0],
        239: pyglet.image.TextureGrid(wall_seq)[9 * 2 + 1],
        255: pyglet.image.TextureGrid(wall_seq)[9 * 3 + 6],
    },
}

tile_highlighter = pyglet.resource.image("highlight.png")

audio = {
    "tile_changed": pyglet.resource.media("audio/tile_changed.wav", streaming=False),
}
