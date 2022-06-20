import re
import math

AcresToSqFt = 43560
divisor = 10
MaxFootprint = 1210

lot_size_row = re.findall("Lot Size\n.*", "Yes\nLot Size\n2,345 Acres\nStyle\nSingle Family Residential\nYear Built")
lot_size = lot_size_row[0].split("\n")[1].strip().replace(",", "")

if "Acres" in lot_size:
    lot_size_in_acres = lot_size.split(" ")[0]
    lot_size = str(math.floor(float(lot_size_in_acres)*AcresToSqFt))

if len(lot_size) > 0:
    if "—" in lot_size:
        Footprint = "ADU cannot be built here."
    else:
        if lot_size.isnumeric():
            usable_lot_size = math.floor(float(lot_size)/divisor)
            if usable_lot_size < MaxFootprint:
                Footprint = str(usable_lot_size) + " Sq. Ft."
            else:
                Footprint = str(MaxFootprint) + " Sq. Ft."

        else:
            Footprint = "ADU cannot be built here."
else:
    Footprint = "Maximum footprint could not be found."


print(Footprint)
