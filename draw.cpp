#include <thread>
#include <stdio.h>
#include <unistd.h>
#include "rotator.h"

extern "C"
{
    class Window {
        private:
            float angle;
            std::thread draw_thread;

            void background(void) {
                run(&angle);
            }
        public:
            int Init(void) {
                angle = 0.f;
                printf("Starting Draw Thread...\n");
                draw_thread = std::thread(&Window::background, this);
                return 0;
            }
            
            int Draw(float new_angle) {
                angle = new_angle;
                return 0;
            }
    };

    void * CreateWindow( void ) {
        return new Window;
    }

    int InitWindow(void *ptr) {
        Window * ref = reinterpret_cast<Window *>(ptr);
        return ref->Init();
    }

    int Draw(void *ptr, float new_angle) {
        Window * ref = reinterpret_cast<Window *>(ptr);
        return ref->Draw(new_angle);
    }
} 
