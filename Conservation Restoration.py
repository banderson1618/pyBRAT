#-------------------------------------------------------------------------------
# Name:        Conservation Restoration
# Purpose:     Adds the conservation and restoration model to the BRAT capacity output
#
# Author:      Jordan Gilbert
#
# Created:     09/2016
# Copyright:   (c) Jordan 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import sys

def main(in_network):

    arcpy.env.overwriteOutput = True


    LowConflict = 0.25
    IntConflict = 0.5
    HighConflict = 0.75

    arcpy.AddField_management(in_network, "oPBRC", "TEXT", "", "", 60)

    cursor = arcpy.da.UpdateCursor(in_network, ["oCC_EX", "oCC_PT", "oPC_Prob", "oPBRC"])
    for row in cursor:

        if row[0] == 0:  # no existing capacity
            if row[1] > 5:
                if row[2] <= IntConflict:
                    row[3] = "Long Term Possibility Restoration Zone"
                else:
                    row[3] = "Unsuitable: Anthropogenically Limited"
            elif row[1] > 1:
                row[3] = "Unsuitable: Anthropogenically Limited"
            else:
                row[3] = "Unsuitable: Naturally Limited"

        elif row[0] > 0 and row[0] <= 1:  # rare existing capacity
            if row[1] > 5:
                if row[2] <= IntConflict:
                    row[3] = "Quick Return Restoration Zone"
                else:
                    row[3] = "Living with Beaver (Low Source)"
            elif row[1] > 1:
                if row[2] <= IntConflict:
                    row[3] = "Long Term Possibility Restoration Zone"
                else:
                    row[3] = "Living with Beaver (Low Source)"
            else:
                row[3] = "Unsuitable: Naturally Limited"

        elif row[0] > 1 and row[0] <= 5:  # occasional existing capacity
            if row[1] > 5:
                if row[2] <= IntConflict:
                    row[3] = "Long Term Possibility Restoration Zone"
                else:
                    row[3] = "Living with Beaver (Low Source)"
            else:
                row[3] = "Unsuitable: Naturally Limited"

        elif row[0] > 5 and row[0] <= 15:  # frequent existing capacity
            if row[1] > 15:
                if row[2] <= IntConflict:
                    row[3] = "Quick Return Restoration Zone"
                else:
                    row[3] = "Living with Beaver (High Source)"
            else:
                if row[2] <= IntConflict:
                    row[3] = "Low Hanging Fruit - Potential Restoration/Conservation Zone"
                else:
                    row[3] = "Living with Beaver (High Source)"

        elif row[0] > 15 and row[0] <= 50: # pervasive existing capacity
            if row[2] <= IntConflict:
                row[3] = "Low Hanging Fruit - Potential Restoration/Conservation Zone"
            else:
                row[3] = "Living with Beaver (High Source)"

        else:
            row[3] = "NOT PREDICTED - Requires Manual Attention"

        cursor.updateRow(row)

    del row
    del cursor

    return in_network

if __name__ == '__main__':
    main(sys.argv[1])
