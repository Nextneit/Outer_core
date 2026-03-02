PYTHON	= python3

all: test

test:
	$(PYTHON) Colleen.py > tmp.py && diff Colleen.py tmp.py && echo "Colleen OK" && rm -f tmp.py
	$(PYTHON) Grace.py && diff Grace.py Grace_kid.py && echo "Grace OK"
	$(PYTHON) Sully.py && echo "Sully OK"

clean:
	rm -f tmp.py

fclean: clean
	rm -f Grace_kid.py Sully_kid.py Sully_*.py

re: fclean all

.PHONY: all test clean fclean re
