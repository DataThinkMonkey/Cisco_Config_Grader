#!/bin/bash
# Jared Bernard
# Grade Cisco config files

clear
# removes white space from beginning of line
modr1file=$(sed 's/^[ \t]*//' "$1" > newr1confg) 
r1file="newr1confg"
# Key file
keyfile="$2"

# separates items in file by new line instead of white space
IFS=$'\n'	
# Heading
echo -e "Score\tKey$(tput cup 0 60)R1 Config"
echo "------------------------------------------------------------------------------------------------ "

totpossible=0
totscore=0
# Loop to create report and score.
for i in $(cat $keyfile)
do 
	row=$(echo "$i")
	score=$(echo "$row" | awk -F',' '{print $2}')
	keyitem=$(echo "$row" | awk -F',' '{print $1}')
	r1item=$(grep $keyitem $r1file)
	
	if [ "$r1item" == "$keyitem"  ]
	then
		# Print each line fo the report
		printf "%0s - %5s %50s\n" $score $keyitem $r1item
		# Must scale and process through bc to keep float int
		totscore=$(echo "scale=2; $totscore + $score" | bc)
#		totpossible=$(echo "scale=2; $totpossible + $score" | bc)

	else
		# print when there is no match in the config file.
		printf "%0s - %5s %50s\n" 0 $keyitem MISSING
		# preserves float int and does not add to total score
		totscore=$(echo "scale=2; $totscore + 0" | bc)
#		totpossible=$(echo "scale=2; $totpossible + $score" | bc)
		
	fi
	totpossible=$(echo "scale=2; $totpossible + $score" | bc)
	 	
done
echo ""
printf "Total Score: %.2f\n" $totscore
printf "Total Possible: %.2f\n" $totpossible
echo ""
echo "Exceptions"
echo "-----------"
grep XXX $keyfile
echo ""
# clean up
rm newr1confg
