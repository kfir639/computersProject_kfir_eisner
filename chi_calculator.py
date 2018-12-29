import math

class ChiCalculator():

    def __init__(self, x, dx, y, dy):
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy

        self.N = len(x)
        self.dy_sum_of_squares = sum([1/(dy_i**2)for dy_i in self.dy])
        self.x_avg = self._get_avg(self.x)
        self.x_squared_avg = self._get_avg([x_i**2 for x_i in self.x])
        self.y_avg = self._get_avg(self.y)
        self.xy_avg = self._get_avg([self.x[i]*self.y[i] for i in range(self.N)])
        self.dy_squared_avg = self._get_avg([dy_i**2 for dy_i in self.dy])

    def _get_avg(self, data_array):
        return sum([data_array[i]/(self.dy[i]**2) for i in range(self.N)]) / self.dy_sum_of_squares

    def get_linear_min_chi_squared(self):
        a = ( self.xy_avg - self.x_avg*self.y_avg ) / ( self.x_squared_avg - self.x_avg**2 )
        da = math.sqrt(
            self.dy_squared_avg / (self.N * ( self.x_squared_avg - self.x_avg**2 ))
        )

        b = self.y_avg - a * self.x_avg
        db = math.sqrt(
            self.dy_squared_avg * self.x_squared_avg / (self.N * ( self.x_squared_avg - self.x_avg**2 ))
        )

        # Calculating Chi2 according to Eq. (3)
        chi_squared = sum([((self.y[i] - a*self.x[i] - b) / self.dy[i])**2 for i in range(self.N)])
        # chi_squared = sum([((self.y[i] - a*self.x[i] - b) / math.sqrt( self.dy[i]**2 + (2*a*self.dx[i])**2))**2
        #                    for i in range(self.N)])
        chi_squared_reduced = chi_squared / (self.N - 2)

        return a, da, b, db, chi_squared, chi_squared_reduced
