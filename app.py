import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
import io

# Define a function to generate a tone for a note with variable duration based on comma usage
def note_to_tone(note, base_duration=500):
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
    note_base = note.split(',')[0].lower()
    extra_commas = note.count(',')  # Count the number of commas
    duration = base_duration + 500 * extra_commas  # Increase duration by 500ms for each comma
    frequency = notes.get(note_base, 261.63)  # Default to C4 if note is not found
    tone = Sine(frequency)
    audio = tone.to_audio_segment(duration=duration)
    return audio

# Function to combine notes into a sequence with extended durations based on commas
def generate_melody(notes_input):
    melody = AudioSegment.silent(duration=0)  # Start with a moment of silence
    for part in notes_input.split():
        tone = note_to_tone(part)
        melody += tone
    return melody

# Streamlit interface
st.title('Musical Note Player')
user_input = st.text_input('Enter a sequence of notes (e.g., "do re mi fa sol la si. Use a comma to double the length (e.g., do mi mi, mi)"):')
if st.button('Generate Tone'):
    melody = generate_melody(user_input)
    # Convert the audio to a format that can be played in the browser
    audio_file = io.BytesIO()
    melody.export(audio_file, format='wav')
    audio_file.seek(0)
    st.audio(audio_file, format='audio/wav', start_time=0)

# Display instructions
st.write('Enter notes separated by spaces. Use commas immediately after a note to increase its duration by 500 ms per comma. Example: "do,, mi, mi" results in "do" played for 1500 ms and "mi" played for 1000 ms.')
