import numpy as np

class TSPInstance:
    def __init__(self, filepath):
        self.filepath = filepath
        self.coords = self._load_coords()

    def _load_coords(self):
        coords = []
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            in_section = False
            for line in lines:
                if line.strip() == 'EOF':
                    break
                if in_section:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        coords.append([float(parts[1]), float(parts[2])])
                if line.strip() == 'NODE_COORD_SECTION':
                    in_section = True
        return np.array(coords)
