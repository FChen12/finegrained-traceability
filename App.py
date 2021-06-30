from Dataset import Etour, Itrust, Smos, EANCI
from TraceabilityBuilder import BaseLineRunner
import Util

F = [0.44]  # Util.get_range_array(0.1, 0.8, 0.1)
M = [0.59]  # Util.get_range_array(0.3, 0.7, 0.1)
b = BaseLineRunner(Etour())
b.precalculate()
b.calculate_f1(F, M)

b = BaseLineRunner(Itrust())
b.precalculate()
b.calculate_f1(F, M)
b = BaseLineRunner(Smos())
b.precalculate()
b.calculate_f1(F, M)
b = BaseLineRunner(EANCI())
b.precalculate()
b.calculate_f1(F, M)