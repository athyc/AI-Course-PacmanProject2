#-p --test test_cases/q4/
#sed -n '1~2!p' q4testerprior.sh > q4tester.sh
sed -i -e 's/^/python autograder.py -p --test test_cases/' q4tester.sh > q4tester1.sh
