import numpy as np
from math import cos, sin, sqrt, pi, asin, acos


class MaskMeshGrid:
    def __init__(self, lat=60, lon=160, step=1 / 60, target_size=(41, 41)):
        self.lat = lat
        self.lon = lon
        self.step = step
        self.target_size = target_size

    @classmethod
    def xyz2gis(cls, x, y, z):
        lat = asin(z) * 180 / pi
        if cos(lat * pi / 180) == 0:
            lon = 0
        else:
            xy = x / cos(lat * pi / 180)
            xy = xy if xy <= 1 else 1
            xy = xy if xy >= -1 else -1
            if y <= 0:
                lon = asin(xy) * 180 / pi
            else:
                lon = asin(xy) * 180 / pi
                if x < 0:
                    lon = -180 - lon
                else:
                    lon = 180 - lon
        return lat, lon

    @classmethod
    def gis2xyz(cls, lat, lon):
        z = sin(lat*pi/180)
        x = cos(lat*pi/180) * sin(lon*pi/180)
        y = -cos(lat*pi/180) * cos(lon*pi/180)
        if abs(x) < 1e-12:
            x = 0
        if abs(y) < 1e-12:
            y = 0
        return x, y, z

    def fetch_grid(self):
        self.lats = [self.lat  - self.step / 2 - self.step * item for item in range(-(self.target_size[0] // 2), self.target_size[0] // 2)]
        self.center_points = [(item, self.lon) if item <= 90 else (180 - item,
                                                                   self.lon - 180 if self.lon - 180 > -180 else self.lon + 180)
                              for item in self.lats]
        gis_grid = []
        for center_point in self.center_points:
            lat, lon = center_point[0], center_point[1]
            x0, y0, z0 = self.gis2xyz(lat, lon)
            p0 = np.array([x0, y0, z0])
            x1, y1, z1 = self.gis2xyz(0, lon - 90)
            p1 = np.array([x1, y1, z1])
            x2, y2, z2 = self.gis2xyz(0, lon + 90)
            p2 = np.array([x2, y2, z2])

            if lon != self.lon:
                p = p1
                p1 = p2
                p2 = p
            numbers = 90 / self.step
            horizontal_points = []
            for i in range(self.target_size[1] // 2, 0, -1):
                alpha1 = (i-1/2) / numbers * pi / 2
                alpha2 = (1 - (i - 1/2) / numbers) * pi / 2
                horizontal_points.append(self.xyz2gis(*(p0 * sin(alpha2) + p1 * sin(alpha1))))
            for i in range(self.target_size[1] // 2):
                alpha1 = (i+1/2) / numbers * pi / 2
                alpha2 = (1 - (i+1/2) / numbers) * pi / 2
                horizontal_points.append(self.xyz2gis(*(p0 * sin(alpha2) + p2 * sin(alpha1))))
            gis_grid.append(horizontal_points)
        return np.array(gis_grid)


if __name__ == "__main__":
    self = MaskMeshGrid(lat=88, lon=0, step=1/60, target_size=(180, 180))
    gis = self.fetch_grid()
    lats, lons = gis[:, :, 0], gis[:, :, 1]
    print(lats.min(), lats.max(), lons.min(), lons.max())

