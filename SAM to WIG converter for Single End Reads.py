import csv

# open a wig file where the output of this code will be saved
output_file = open('Stranded RNA-Seq of Pulldown cabRNA from phi80alpha infection of RN4220 expressing Ssc-CdnE03.wig', 'w')

# create a header needed in the wig file
output_file.write(
    "track" + "\t" + "type=wiggle_0" + "\n" + "color" + "\t" + "5:150:55" + "\t" + "225:0:0" + "\n" + "variableStep" + "\t" + "chrom=phi80alpha-vir" + "\t" + "span=1" + "\n")

# create empty dictionary to save mapping data with keys for every bp position and values for the number of reads mapped at that bp
for_strand = {}

# fill the dictionary with keys for each bp and items to 0
key_bp = 1
for_strand[key_bp] = 0
# here change the value to the genome size (e.g phi80alpha-vir = 43853bp, last 151 manually add to the first 151nt)
while key_bp != 44004:
    key_bp = int(key_bp + 1)
    for_strand[key_bp] = 0

counter=0
# open the SAM file and specify that the file has tab delimitation
with open('Stranded RNA-Seq of Pulldown cabRNA from phi80alpha infection of RN4220 expressing Ssc-CdnE03.sam') as sam_file:
    sam_reader = csv.reader(sam_file, delimiter='\t')

    # skip 3 line header of SAM file generated from Bowtie2
    skip_firstline = next(sam_reader)
    skip_secondline = next(sam_reader)
    skip_thirdline = next(sam_reader)

    # loop through each line of the SAM file starting at line 4
    for line in sam_reader:


        # if the line is labeled 0, reads are aligned to top strand of phi80alpha-vir
        # the code will retrieve the starting and end position and will add 1 to each bp location associated with that
        if int(line[1]) == 0:
            print(str(line[0]))
            for bp in range(int(line[3]), ((int(len(line[9]))) + int(line[3]))):
                for_strand[bp] += 1

        # same as above, but if the line is labeled 16, reads are aligned to bottom strand of phi80alpha-vir
        elif int(line[1]) == 16:
            print(str(line[0]))
            for bp in range(int(line[3]), ((int(len(line[9]))) + int(line[3]))):
                for_strand[bp] += 1

        # if the line is not labeled 0 nor 16, that means it was not aligned to the genome, so skip
        else:
            pass

for bp, read in for_strand.items():


    # write a line in the output file containing the bp location and then the forward and reverse read value
    output_file.write(str(bp) + "\t" + str(read) + "\n")

output_file.close()

# 0 is top strand
# 16 is bottom strannd

