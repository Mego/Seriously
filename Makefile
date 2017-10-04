seriously: main.o SeriousFloat.o SeriousFunction.o SeriousInteger.o SeriousList.o SeriousObject.o SeriousString.o
		g++ -o main main.o SeriousFloat.o SeriousFunction.o SeriousInteger.o SeriousList.o SeriousObject.o SeriousString.o

main.o: main.cpp
		g++ -c main.cpp -I ./include

SeriousFloat.o: src/SeriousFloat.cpp
		g++ -c src/SeriousFloat.cpp -I ./include

SeriousInteger.o: src/SeriousInteger.cpp
		g++ -c src/SeriousInteger.cpp -I ./include

SeriousList.o: src/SeriousList.cpp
		g++ -c src/SeriousList.cpp -I ./include

SeriousObject.o: src/SeriousObject.cpp
		g++ -c src/SeriousObject.cpp -I ./include

SeriousString.o: src/SeriousString.cpp
		g++ -c src/SeriousString.cpp -I ./include

SeriousFunction.o: src/SeriousFunction.cpp
		g++ -c src/SeriousFunction.cpp -I ./include

clean:
		rm main *.o