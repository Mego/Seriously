seriously: main.o SeriousFloat.o SeriousFunction.o SeriousInteger.o SeriousList.o SeriousObject.o SeriousString.o
		$(CXX) -o main main.o SeriousFloat.o SeriousFunction.o SeriousInteger.o SeriousList.o SeriousObject.o SeriousString.o

main.o: main.cpp
		$(CXX) -c main.cpp -I ./include

SeriousFloat.o: src/SeriousFloat.cpp
		$(CXX) -c src/SeriousFloat.cpp -I ./include

SeriousInteger.o: src/SeriousInteger.cpp
		$(CXX) -c src/SeriousInteger.cpp -I ./include

SeriousList.o: src/SeriousList.cpp
		$(CXX) -c src/SeriousList.cpp -I ./include

SeriousObject.o: src/SeriousObject.cpp
		$(CXX) -c src/SeriousObject.cpp -I ./include

SeriousString.o: src/SeriousString.cpp
		$(CXX) -c src/SeriousString.cpp -I ./include

SeriousFunction.o: src/SeriousFunction.cpp
		$(CXX) -c src/SeriousFunction.cpp -I ./include

clean:
		rm main *.o