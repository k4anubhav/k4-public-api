from typing import Dict

import requests
from PIL import Image, ImageDraw, ImageFont


def truncate(s: str, limit: int) -> str:
    s = s.strip()
    if len(s) > limit:
        return s[:limit - 1].strip() + '...'
    return s


class SpotifyBanner:
    def __init__(
            self,
            playing_track: Dict,
            background_color: str = "#000000",
            heading_color: str = "#FFFFFF",
            subheading_color: str = "#B3B3B3",
    ):
        self._playing_track = playing_track
        self.background_color = background_color
        self.heading_color = heading_color
        self.subheading_color = subheading_color
        self._banner = None

    @property
    def banner(self):
        if self._banner:
            return self._banner

        track = self._playing_track['item']
        image = Image.new("RGB", (1000, 300), color=self.background_color)
        font_heading = ImageFont.truetype(r'doc/spotify/GILLSANS.ttf', 30)
        font_subheading = ImageFont.truetype(r'doc/spotify/GILLSANS-ITALIC.ttf', 20)

        draw = ImageDraw.Draw(image)

        track_image = Image.open(requests.get(track['album']['images'][0]['url'], stream=True).raw).resize(
            (300, 300), Image.ANTIALIAS
        )

        image.paste(track_image, (0, 0))
        heading = truncate(track['name'], 26)
        subheading = truncate(track['artists'][0]['name'], 45)

        draw.text((310, 10), heading, fill=self.heading_color, font=font_heading)
        draw.text((312, 40), subheading, fill=self.subheading_color, font=font_subheading)

        if self._playing_track['is_playing']:
            play_pause = Image.open(r'doc/spotify/play.png')
        else:
            play_pause = Image.open(r'doc/spotify/pause.png')
        image.paste(play_pause.resize((20, 20)), (310, 270))

        progress = self._playing_track['progress_ms'] / self._playing_track['item']['duration_ms']

        progress_start = (340, 270)
        progress_end = (980, 270)
        progress_height = 20
        progress_width = progress_end[0] - progress_start[0]
        progress_bar = Image.new("RGB", (progress_width, progress_height), color=self.subheading_color)
        image.paste(progress_bar, progress_start)
        progress_bar = Image.new("RGB", (int(progress_width * progress), progress_height), color="#1DB954")
        image.paste(progress_bar, progress_start)

        return image

    def __str__(self):
        return f"{self._playing_track['item']['name']}"
