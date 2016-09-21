SOURCES = draw.cpp rotator.cpp camera.cpp cameracontrol.cpp graphics.cpp input.cpp
INCLUDE = -I/opt/vc/include -I/opt/vc/userland-master/interface/vcos -I/opt/vc/userland-master -I/opt/vc/userland-master/interface/vcos/pthreads -I/opt/vc/userland-master/interface/vmcs_host/linux -I/opt/vc/userland-master/host_applications/linux/libs/bcm_host/include
LIBRARY = -L/opt/vc/lib
LINKED = -l:libmmal_core.so -l:libmmal_util.so -l:libmmal_vc_client.so -l:libvcos.so -l:libbcm_host.so -lGLESv2 -lEGL

build:
	gcc $(INCLUDE) $(LIBRARY) $(LINKED) -pthread -shared -o draw.so -fPIC -Wall -lstdc++ $(SOURCES)

clean:
	rm -f *.so

