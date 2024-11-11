import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
import io

# Define a function to generate a tone for a note with complex duration specifications
def note_to_tone(note_spec, base_duration=500):
    # Note frequencies in Hz (simplified)
    notes = {
        'do-1': 130.81,  # C3
        're-1': 146.83,  # D3
        'mi-1': 164.81,  # E3
        'fa-1': 174.61,  # F3
        'sol-1': 196.00,  # G3
        'la-1': 220.00,  # A3
        'si-1': 246.94,  # B3
        
        'do': 261.63,  # C4
        're': 293.66,  # D4
        'mi': 329.63,  # E4
        'fa': 349.23,  # F4
        'sol': 392.00,  # G4
        'la': 440.00,  # A4
        'si': 493.88,  # B4
    
        'do1': 523.25,  # C5
        're1': 587.33,  # D5
        'mi1': 659.25,  # E5
        'fa1': 698.46,  # F5
        'sol1': 783.99,  # G5
        'la1': 880.00,  # A5
        'si1': 987.77,  # B5
    }

    
    # Split note and duration or comma additions
    parts = note_spec.split(':')
    note_part = parts[0]
    extra_commas = note_part.count(',')
    note_base = note_part.split(',')[0].lower()

    # Set duration based on colon or comma usage
    if len(parts) > 1:
        duration = int(parts[1])  # User specified duration overrides comma additions
    else:
        duration = base_duration + 500 * extra_commas  # Increment duration for each comma

    # Get frequency and generate tone
    frequency = notes.get(note_base, 261.63)  # Default to C4 if note is not found
    tone = Sine(frequency)
    audio = tone.to_audio_segment(duration=duration)
    return audio

# Function to combine notes into a sequence with specified durations
def generate_melody(notes_input):
    melody = AudioSegment.silent(duration=0)  # Start with a moment of silence
    for part in notes_input.split():
        tone = note_to_tone(part)
        melody += tone
    return melody

# Streamlit interface
st.title('Create Your Melody')
st.caption('Sample to copy and paste: do re mi do do re mi do mi fa sol, mi fa sol, sol:250 la:250 sol:250 fa:250 mi do sol:250 la:250 sol:250 fa:250 mi do do sol-1 do, do sol-1 do,')
user_input = st.text_input('Enter a sequence of notes (e.g., "do:1000, mi,, mi:750"): if you simply write "do re mi", the default duration is 500 ms. Using a comma doubles the duration.', '')

if st.button('Generate Tone'):
    melody = generate_melody(user_input)
    # Convert the audio to a format that can be played in the browser
    audio_file = io.BytesIO()
    melody.export(audio_file, format='wav')
    audio_file.seek(0)
    st.audio(audio_file, format='audio/wav', start_time=0)

# Display notes and instructions
table_markdown = """
| note Symbol | Frequency (Hz) | Octave |
|------|----------------|--------|
| do-1 | 130.81         | C3     |
| re-1 | 146.83         | D3     |
| mi-1 | 164.81         | E3     |
| fa-1 | 174.61         | F3     |
| sol-1| 196.00         | G3     |
| la-1 | 220.00         | A3     |
| si-1 | 246.94         | B3     |
| do   | 261.63         | C4     |
| re   | 293.66         | D4     |
| mi   | 329.63         | E4     |
| fa   | 349.23         | F4     |
| sol  | 392.00         | G4     |
| la   | 440.00         | A4     |
| si   | 493.88         | B4     |
| do1  | 523.25         | C5     |
| re1  | 587.33         | D5     |
| mi1  | 659.25         | E5     |
| fa1  | 698.46         | F5     |
| sol1 | 783.99         | G5     |
| la1  | 880.00         | A5     |
| si1  | 987.77         | B5     |
"""

st.markdown(table_markdown)
