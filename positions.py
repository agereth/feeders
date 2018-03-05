import csv
import sys

Ref = 0
Val = 1
Package = 2
PosX = 3
PosY = 4
Rot = 5
Side = 6
Nozzle = 1
Stack = 2
Height = 3
Speed = 4
Vision = 5
Pressure = 6


def create_csv(filename: str, side: str, pos_data: [str], feeder_data: [str]):
    """
    creates csv for machine for top or bottom side of board
    :param filename: filename for csv
    :param side: top or bottom
    :param pos_data: list of positoins
    :param feeder_data: list of feeders
    :return:
    """
    f = open(filename.split('.')[0] + "_%s.csv" % side, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(
        ['Designator', "NozzleNum", "StackNum", "Mid X", "Mid Y", "Rotation", "Height", "Speed", "Vision", "Pressure",
         "Explanation"])
    for pos in pos_data:
        current_pos = '%s %s' % (pos[Package], pos[Val])
        if "FuseShorted" in current_pos or "Logo" in current_pos or "TEST" in current_pos:
            continue
        current_feeder = None
        for feeder in feeder_data:
            if feeder[0] == current_pos:
                current_feeder = feeder
        if not current_feeder:
            current_feeder = [current_pos, '1', 'L1', '0', '100', 'None']
        row = [pos[Ref], current_feeder[Nozzle], current_feeder[Stack], pos[PosX], pos[PosY], pos[Rot],
               current_feeder[Height], current_feeder[Speed], current_feeder[Vision], 'True',
               current_pos]
        writer.writerow(row)
    f.close()


def main(filename: str):
    try:
        f = open(filename)
    except FileNotFoundError:
        print("File %s not found" % filename)
        raise
    reader = csv.reader(f)
    pos_data = [row for row in reader][1:]
    top_data = [pos[:Side] for pos in pos_data if pos[Side] == 'top']
    bottom_data = [pos[:Side] for pos in pos_data if pos[Side] == 'bottom']
    f.close()
    try:
        f = open("Feeders.csv")
    except FileNotFoundError:
        print("File Feeders.csv does not exist")
        raise
    reader = csv.reader(f, delimiter=';')
    feeder_data = [row for row in reader][1:]
    feeder_data = [row for row in feeder_data if row[0]]
    f.close()
    create_csv(filename, "top", top_data, feeder_data)
    create_csv(filename, "bottom", bottom_data, feeder_data)
    return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Name of positions file not specified")
