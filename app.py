import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
import io

# Define a function to generate a tone for a note
def note_to_tone(note, duration=500):
    # Note frequencies in Hz (simplified)
    notes = {
        'do': 261.63,  # C4
        're': 293.66,  # D4
        'mi': 329.63,  # E4
        'fa': 349.23,  # F4
        'sol': 392.00,  # G4
        'la': 440.00,  # A4
        'si': 493.88   # B4
    }
    frequency = notes.get(note, 261.63)  # Default to C4 if note is not found
    tone = Sine(frequency)
    audio = tone.to_audio_segment(duration=duration)
    return audio

# Function to combine notes into a sequence
def generate_melody(notes_input):
    parts = notes_input.split()
    melody = AudioSegment.silent(duration=0)  # Start with a moment of silence
    for part in parts:
        tone = note_to_tone(part)
        melody += tone
    return melody

# Streamlit interface
st.title('Musical Note Player')
user_input = st.text_input('Enter a sequence of notes (do, re, mi, fa, sol, la, si):', 'do mi mi')
if st.button('Generate Tone'):
    melody = generate_melody(user_input)
    # Convert the audio to a format that can be played in the browser
    audio_file = io.BytesIO()
    melody.export(audio_file, format='wav')
    audio_file.seek(0)
    st.audio(audio_file, format='audio/wav', start_time=0)

# Display instructions
st.write('Enter notes separated by spaces. Example: "do re mi fa sol".')
