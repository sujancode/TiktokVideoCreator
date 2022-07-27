from pathlib import Path
import random
from random import randrange
from typing import Any, Tuple


from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube
from pytube.cli import on_progress


# Supported Background. Can add/remove background video here....
# <key>-<value> : key -> used as keyword for TOML file. value -> background configuration
# Format (value):
# 1. Youtube URI
# 2. filename
# 3. Citation (owner of the video)
# 4. Position of image clips in the background. See moviepy reference for more information. (https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html#moviepy.video.VideoClip.VideoClip.set_position)
background_options = {
    "motor-gta": (  # Motor-GTA Racing
        "https://www.youtube.com/watch?v=vw5L4xCPy9Q",
        "bike-parkour-gta.mp4",
        "Achy Gaming",
        lambda t: ("center", 480 + t),
    ),
    "rocket-league": (  # Rocket League
        "https://www.youtube.com/watch?v=2X9QGY__0II",
        "rocket_league.mp4",
        "Orbital Gameplay",
        lambda t: ("center", 200 + t),
    ),
    "minecraft": (  # Minecraft parkour
        "https://www.youtube.com/watch?v=n_Dv4JMiwK8",
        "parkour.mp4",
        "bbswitzer",
        "center",
    ),
    "gta": (  # GTA Stunt Race
        "https://www.youtube.com/watch?v=qGa9kWREOnE",
        "gta-stunt-race.mp4",
        "Achy Gaming",
        lambda t: ("center", 480 + t),
    ),
}


def get_start_and_end_times(video_length: int, length_of_clip: int) -> Tuple[int, int]:
    """Generates a random interval of time to be used as the background of the video.

    Args:
        video_length (int): Length of the video
        length_of_clip (int): Length of the video to be used as the background

    Returns:
        tuple[int,int]: Start and end time of the randomized interval
    """
    random_time = randrange(180, int(length_of_clip) - int(video_length))
    return random_time, random_time + video_length


def get_background_config(background_choice):
    """Fetch the background/s configuration"""
    try:
        choice = str(background_choice).casefold()
    except AttributeError:
        print("No background selected. Picking random background'")
        choice = None

    # Handle default / not supported background using default option.
    # Default : pick random from supported background.
    if not choice or choice not in background_options:
        choice = random.choice(list(background_options.keys()))

    return background_options[choice]


def download_background(background_config: Tuple[str, str, str, Any]):
    """Downloads the background/s video from YouTube."""
    Path("./assets/backgrounds/").mkdir(parents=True, exist_ok=True)
    # note: make sure the file name doesn't include an - in it
    uri, filename, credit, _ = background_config
    if Path(f"assets/backgrounds/{credit}-{filename}").is_file():
        return
    print(
        "We need to download the backgrounds videos. they are fairly large but it's only done once. 😎"
    )
    print("Downloading the backgrounds videos... please be patient 🙏 ")
    print(f"Downloading {filename} from {uri}")
    YouTube(uri, on_progress_callback=on_progress).streams.filter(res="1080p").first().download(
        "assets/backgrounds", filename=f"{credit}-{filename}"
    )
    print("Background videos downloaded successfully! 🎉")


def chop_background_video(background_config: Tuple[str, str, str, Any], video_length: int,username):
    """Generates the background footage to be used in the video and writes it to assets/temp/background.mp4

    Args:
        background_config (Tuple[str, str, str, Any]) : Current background configuration
        video_length (int): Length of the clip where the background footage is to be taken out of
    """

    print("Finding a spot in the backgrounds video to chop...✂️")
    choice = f"{background_config[2]}-{background_config[1]}"

    background = VideoFileClip(f"assets/backgrounds/{choice}")

    start_time, end_time = get_start_and_end_times(video_length, background.duration)
    try:
        ffmpeg_extract_subclip(
            f"assets/backgrounds/{choice}",
            start_time,
            end_time,
            targetname=f"assets/temp/{username}/background.mp4",
        )
    except (OSError, IOError):  # ffmpeg issue see #348
        print("FFMPEG issue. Trying again...")
        with VideoFileClip(f"assets/backgrounds/{choice}") as video:
            new = video.subclip(start_time, end_time)
            new.write_videofile(f"assets/{username}/temp/background.mp4")
    print("Background video chopped successfully!")
    return background_config[2]
