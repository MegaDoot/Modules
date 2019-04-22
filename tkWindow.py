from tkinter import Tk

class Window(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.build():
            self.mainloop()

    @staticmethod
    def _interpret_weight_arg(val, grid_dim):
        if hasattr(val, "__iter__"):
            return val
        
        if isinstance(val, (bool, int)):
            if not val:
                return ()
            elif val == True or val > grid_dim:
                val = grid_dim
            elif val < 0:
                return range(grid_dim - 1, grid_dim + val - 1, -1)
            return range(val)

        raise TypeError("No way to intepret "+str(type(val))+" as list of columns/rows")

    dims = ("column", "row")
    
    def gridconfigure(self, dim, *args, **kwargs):
        return getattr(self, self.dims[dim]+"configure")(*args, **kwargs)
                
    def give_weight(self, cols = True, rows = True):
        grid_size = self.grid_size()

        weighted = (
            self._interpret_weight_arg(cols, grid_size[0]),
            self._interpret_weight_arg(rows, grid_size[1]))

        for dim in range(len(grid_size)):
            for i in range(grid_size[dim]):
                self.gridconfigure(dim, i, weight = 1 if i in weighted[dim] else 0)
    
    def build(self):
        """
        Overwrite to add widgets before mainloop
        Return a truthy value to stop mainloop auto-triggering
        """
        pass