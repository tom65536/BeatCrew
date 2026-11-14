import struct
import wave
from pathlib import Path

import wubwub

SAMPLE_WAV = Path(__file__).with_name("22417__lunardrive__single-heartbeat-hq_beatsmith.wav")


BPM = 120
BARS = 4
BEATS_PER_BAR = 4

OUTPUT_PATH = Path(__file__).with_name("b4_metal_blast.wav")


def render_sequence():
	with wave.open(str(SAMPLE_WAV), "rb") as source:
		channels = source.getnchannels()
		sample_rate = source.getframerate()
		sample_width = source.getsampwidth()
		if source.getcomptype() != "NONE" or sample_width != 2:
			raise ValueError("The source must be an uncompressed 16-bit PCM WAV file")
		source_samples = struct.unpack("<" + "h" * (source.getnframes() * channels), source.readframes(source.getnframes()))

	total_beats = BARS * BEATS_PER_BAR
	total_frames = round(total_beats * 60 / BPM * sample_rate)
	mix = [0] * (total_frames * channels)
	frames_per_beat = round(60 / BPM * sample_rate)

	# Notes are numbered from 1, so every fourth note starts on beat 3, 7, 11, ...
	for beat in range(2, total_beats, 4):
		start = beat * frames_per_beat * channels
		count = min(len(source_samples), len(mix) - start)
		for index in range(count):
			mix[start + index] += source_samples[index]

	pcm = struct.pack("<" + "h" * len(mix), *(max(-32768, min(32767, sample)) for sample in mix))
	with wave.open(str(OUTPUT_PATH), "wb") as output:
		output.setnchannels(channels)
		output.setsampwidth(2)
		output.setframerate(sample_rate)
		output.writeframes(pcm)


if __name__ == "__main__":
	render_sequence()
