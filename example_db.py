import yaml
from handler.EarthlingDBPool import exec
exec(f"UPDATE anytable SET anyvar = {anytext} ... ")
result = exec(f"SELECT * from anytable where idx={anyidx}")