typedef short int SAMPLE;
typedef float CSAMPLE;
#include <rubberband/RubberBandStretcher.h>
#include "audio.h"

using RubberBand::RubberBandStretcher;
#include <SDL2/SDL.h>

#define MUS_PATH "/home/mark25/test.wav"
#define BUFFER 32768
#define CHANNELS 1

// prototype for our audio callback
// see the implementation for more information
void my_audio_callback(void *userdata, Uint8 *stream, int len);

// variable declarations
static Uint8 *wav_buffer; // buffer containing our audio file
static Uint8* audio_pos;
static int audio_len; // remaining length of the sample we have to play
int playpos = 0;
float cbuffer[1][BUFFER];
RubberBand::RubberBandStretcher* rb;
float *obuffer[1];

/*
** PLAYING A SOUND IS MUCH MORE COMPLICATED THAN IT SHOULD BE
*/
void init_audio(){

        printf("Initializing audio...\n");
	// Initialize SDL.
	if (SDL_Init(SDL_INIT_AUDIO) < 0)
			return;

	// local variables
	static Uint32 wav_length; // length of our sample
	static SDL_AudioSpec wav_spec, output_spec;
	
	
	/* Load the WAV */
	// the specs, length and buffer of our wav are filled
	if( SDL_LoadWAV(MUS_PATH, &wav_spec, &wav_buffer, &wav_length) == NULL ){
	  return;
	}
	// set the callback function
	wav_spec.format = AUDIO_S16LSB;
	wav_spec.channels = 1;
	wav_spec.samples = BUFFER;
	wav_spec.freq = 44100;
	output_spec.callback = my_audio_callback;
	output_spec.userdata = NULL;
	output_spec.format = AUDIO_S16LSB;
	output_spec.channels = 1;
	output_spec.samples = BUFFER;
	output_spec.freq = 44100;
	// set our global static variables
	audio_pos = wav_buffer;
	audio_len = wav_length; // copy file length

	printf("Allocating output buffers\n");
	obuffer[0] = new float[BUFFER];
	printf("Creating time stretcher\n");
	rb = new RubberBandStretcher(44100,1,RubberBandStretcher::OptionProcessRealTime,1.0,1.0);

	/* Open the audio device */
	if ( SDL_OpenAudio(&output_spec, NULL) < 0 ){
	  fprintf(stderr, "Couldn't open audio: %s\n", SDL_GetError());
	  exit(-1);
	}
	
	/* Start playing */
	SDL_PauseAudio(0);
}

void my_audio_callback(void *userdata, Uint8 *stream, int len) {
	printf("Making %d samples/%d\n", len, audio_len);
	if (playpos + len > audio_len) {
		len = audio_len - playpos;
	}
	printf("A\n");
	for (int i = 0; i < len; ++i) {
		cbuffer[0][i] = *((Sint16*)audio_pos[i]);
	}
	printf("B\n");
	playpos += len*2;
	if (playpos >= audio_len) {
        	playpos = 0;
	}
	float *ptrs[1];
	ptrs[0] = cbuffer[0];
	rb->process((const float* const*)ptrs, len, false);
        int frames_available = rb->available();

	int outchunk = std::min(frames_available, len);
        int received_frames = rb->retrieve((float* const*)obuffer, outchunk);

	printf("Setting %d channels and %d samples\n", CHANNELS, received_frames);
        for (int i = 0; i < received_frames; ++i) {
		stream[i*2] = (Sint16)obuffer[0][i];
	}
}

void set_audio_speed(float speed) {
	rb->setPitchScale(speed);
}

void close_audio() {
	printf("Audio complete!\n");
	// shut everything down
	SDL_CloseAudio();
	SDL_FreeWAV(wav_buffer);
}
