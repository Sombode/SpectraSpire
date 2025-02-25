import sys

def read_file(filename):
    prependCommas = False
    with open(filename, 'r') as file:
        with open('output.txt', 'w') as output_file:
            line = file.readline()
            while(line):
                # Each spectrum block starts with the name, so blocks are found by looking for lines starting with "Name: "
                if(line.startswith("Name: ")):
                    # Start reading spectrum data
                    name = line.split(": ")[1].strip();
                    while(line and not line.startswith("Formula:")):
                        line = file.readline()
                    formula = line.split(": ")[1].strip();
                    while(line and not line.startswith("ExactMass:")):
                        line = file.readline()
                    mass = round(float(line.split(": ")[1].strip()), 3);
                    # Num Peaks is only used as a marker for the start of the peak data, so it isn't stored
                    while(line and not line.startswith("Num Peaks:")):
                            line = file.readline()
                    peaks = []
                    line = file.readline()
                    while(line and not line == "\n"):
                        for peak in line.split(";"):
                            peak = peak.strip()
                            if peak == "": continue
                            pos = peak.split(" ")[0]
                            val = peak.split(" ")[1]
                            if(int(val) > 0):
                                peaks.append((pos, val))
                        line = file.readline()
                    
                    # To simplify search using SpectraSpire, peaks are sorted form highest to lowest intensity during encoding
                    peaks = sorted(peaks, key=lambda peak: float(peak[1]), reverse=True)

                    # Turn the peaks list into two String (one for positions, another for intensities)
                    peakPosStr = "{"
                    peakValStr = "{"
                    _prependCommas = False
                    for peak in peaks:
                        if(_prependCommas):
                            peakPosStr += ","
                            peakValStr += ","
                        _prependCommas = True
                        peakPosStr += peak[0]
                        peakValStr += peak[1]
                    peakPosStr += "}"
                    peakValStr += "}"

                    if(prependCommas):
                        output_file.write(",")
                    prependCommas = True
                    output_file.write("{" + f'"{name}","{formula}","{mass}",{peakPosStr},{peakValStr}' + "}")
                line = file.readline()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    read_file(filename)