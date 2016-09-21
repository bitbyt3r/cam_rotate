SOURCES = draw.cpp

build:
	gcc -pthread -shared -o draw.so -fPIC -Wall -lstdc++ $(SOURCES)

clean:
	rm -f *.so
