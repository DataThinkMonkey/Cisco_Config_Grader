#!/bin/bash
# Jared Bernard
# Grade Cisco config files

read -p "Which device would you like graded (i.e. r1, r2, s1, etc)?: " device

case $device in
    r1) 
        config="r1-confg"
        key="r1-key.txt";;
    r2)
        config="r2-confg"
        key="r2-key.txt";;
    r3)
        config="r3-confg"
        key="r3-key.txt";;
    s1)
        config="s1-confg"
        key="s1-key.txt";;
    s2)
        config="s2-confg"
        key="s2-key.txt";;
    s3)
        config="s3-confg"
        key="s3-key.txt";;
    *)
        echo "Please select either r1, r2, r3, s1, s2 or s3."
esac


clear
# removes white space from beginning of line
modr1file=$(sed 's/^[ \t]*//' "$config" > newr1confg) 
r1file="newr1confg"
# Key file
keyfile="$key"

# separates items in file by new line instead of white space
IFS=$'\n'	
# Heading
echo -e "Score\tKey$(tput cup 0 60)$device Config"
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
