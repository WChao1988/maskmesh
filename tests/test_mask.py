import numpy as np
import pytest

from maskmesh import MaskMeshGrid


class TestCoordinateHelpers:
    @pytest.mark.parametrize(
        "lat,lon",
        [
            (0.0, 0.0),
            (60.0, 160.0),
            (-45.0, -30.0),
            (88.0, 179.0),
        ],
    )
    def test_gis2xyz_xyz2gis_roundtrip(self, lat, lon):
        x, y, z = MaskMeshGrid.gis2xyz(lat, lon)
        lat2, lon2 = MaskMeshGrid.xyz2gis(x, y, z)
        assert abs(lat2 - lat) < 1e-9
        assert abs(((lon2 - lon + 180.0) % 360.0) - 180.0) < 1e-9

    def test_gis2xyz_unit_vectors(self):
        for lat in (-90, -30, 0, 30, 90):
            for lon in (-180, -90, 0, 90, 180):
                x, y, z = MaskMeshGrid.gis2xyz(lat, lon)
                assert abs(np.linalg.norm([x, y, z]) - 1.0) < 1e-12


class TestFetchGrid:
    def test_shape_even_target_size(self):
        gis = MaskMeshGrid(lat=60, lon=160, step=1 / 60, target_size=(60, 60)).fetch_grid()
        assert gis.shape == (60, 60, 2)

    def test_shape_odd_target_size_truncated_to_even(self):
        gis = MaskMeshGrid().fetch_grid()
        assert gis.shape == (40, 40, 2)

    def test_grid_is_centered(self):
        # the grid is symmetric around the center: the midpoint of the two
        # innermost cells (straddling the center) equals the requested center
        lat, lon = 60.0, 160.0
        gis = MaskMeshGrid(lat=lat, lon=lon, step=1 / 60, target_size=(60, 60)).fetch_grid()
        mid = (gis[29, 29] + gis[30, 30]) / 2
        assert abs(mid[0] - lat) < 1e-4
        assert abs(mid[1] - lon) < 1e-4

    def test_column_step_matches_step(self):
        step = 1 / 60
        gis = MaskMeshGrid(lat=0, lon=0, step=step, target_size=(40, 40)).fetch_grid()
        diffs = np.diff(gis[0, :, 1])
        assert np.allclose(diffs, step, atol=1e-6)

    def test_latitudes_within_bounds(self):
        gis = MaskMeshGrid(lat=88, lon=0, step=1 / 60, target_size=(180, 180)).fetch_grid()
        assert gis[..., 0].min() >= -90.0
        assert gis[..., 0].max() <= 90.0
        assert gis[..., 1].min() >= -180.0
        assert gis[..., 1].max() <= 180.0

    def test_deterministic(self):
        make = lambda: MaskMeshGrid(lat=30, lon=-120, step=0.5, target_size=(20, 20)).fetch_grid()
        assert np.array_equal(make(), make())
