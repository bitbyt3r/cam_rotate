#include <thread>
#include <stdio.h>
#include <unistd.h>
#include "rotator.h"
#include "audio.h"

extern "C"
{
    class Window {
        private:
            float angle, scale, icx, icy, scx, scy;
            std::thread draw_thread;

            void background(void) {
                run(&angle, &scale, &icx, &icy, &scx, &scy);
            }
        public:
            int Init(void) {
                angle = 0.f;
                printf("Starting Draw Thread...\n");
                draw_thread = std::thread(&Window::background, this);
                //init_audio();
                return 0;
            }
            
            int Draw(float new_angle) {
                angle = new_angle;
                return 0;
            }

            int Config(float newscale, float newicx, float newicy, float newscx, float newscy) {
                scale = newscale;
                icx = newicx;
                icy = newicy;
                scx = newscx;
                scy = newscy;
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

    int Config(void *ptr, float scale, float icx, float icy, float scx, float scy) {
        Window * ref = reinterpret_cast<Window *>(ptr);
        return ref->Config(scale, icx, icy, scx, scy);
    }
} 
