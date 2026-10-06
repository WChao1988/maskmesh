# maskmesh

[![PyPI](https://img.shields.io/pypi/v/maskmesh)](https://pypi.org/project/maskmesh/)
[![Python](https://img.shields.io/pypi/pyversions/maskmesh)](https://pypi.org/project/maskmesh/)
[![License: MIT](https://img.shields.io/pypi/l/maskmesh)](LICENSE)
[![CI](https://github.com/WChao1988/maskmesh/actions/workflows/ci.yml/badge.svg)](https://github.com/WChao1988/maskmesh/actions/workflows/ci.yml)

`maskmesh` builds regular latitude/longitude mesh grids **centered on an arbitrary point on the sphere**.

Grid points are interpolated on the sphere (via 3D unit-vector arcs) instead of naive flat addition, so grids stay seamless when they cross the **poles** (latitude wrap beyond ±90°) or the **±180° antimeridian** — handy for regional masks, meteorological/climate data extraction, and anywhere you need a local equidistant grid anywhere on the globe.

## Features

- Rectangular (lat, lon) grids centered on any `(lat, lon)`, with a fixed angular `step` (degrees)
- Seamless wrap-around across the poles and the antimeridian
- Bidirectional coordinate helpers between (lat, lon) and unit-sphere (x, y, z)
- Pure Python + NumPy, no compiled dependencies

## Installation

```bash
pip install maskmesh
```

Or from source:

```bash
git clone https://github.com/WChao1988/maskmesh.git
cd maskmesh
pip install .
```

## Quick start

```python
from maskmesh import MaskMeshGrid

grid = MaskMeshGrid(lat=60, lon=160, step=1/60, target_size=(60, 60))

gis = grid.fetch_grid()          # ndarray of shape (60, 60, 2)
lats, lons = gis[..., 0], gis[..., 1]
```

A grid centered near the antimeridian wraps around instead of breaking:

```python
grid = MaskMeshGrid(lat=0, lon=179.9, step=1/60, target_size=(40, 40))
lons = grid.fetch_grid()[..., 1]
# longitudes smoothly span ~179.6 ... 180 -> -180 ... -179.6
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `lat` | `60` | Center latitude in degrees |
| `lon` | `160` | Center longitude in degrees |
| `step` | `1/60` | Grid step in degrees (1/60 = 1 arcminute) |
| `target_size` | `(41, 41)` | Nominal grid size `(rows, cols)` |

> **Note:** rows and columns are generated as symmetric ±half-step pairs around the
> center, so the returned array always has even side lengths: a `target_size` of
> `(41, 41)` yields a `(40, 40, 2)` array, `(180, 180)` yields `(180, 180, 2)`.

### Coordinate helpers

```python
x, y, z = MaskMeshGrid.gis2xyz(lat, lon)   # (lat, lon) -> unit sphere (x, y, z)
lat, lon = MaskMeshGrid.xyz2gis(x, y, z)   # unit sphere (x, y, z) -> (lat, lon)
```

## Development

```bash
pip install -e .[dev]
pytest
```

## License

[MIT](LICENSE)
