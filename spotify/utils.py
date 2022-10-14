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
            text_color: str = "#FFFFFF",
    ):
        self._playing_track = playing_track
        self.background_color = background_color
        self.text_color = text_color
        self._banner = None

    @property
    def banner(self):
        if self._banner:
            return self._banner

        track = self._playing_track['item']
        image = Image.new("RGB", (1000, 300), color=self.background_color)
        font_heading = ImageFont.truetype(r'GILLSANS.ttf', 50)
        font_subheading = ImageFont.truetype(r'GILLSANS.ttf', 30)

        draw = ImageDraw.Draw(image)

        track_image = Image.open(requests.get(track['album']['images'][0]['url'], stream=True).raw).resize(
            (300, 300), Image.ANTIALIAS
        )

        heading = truncate(track['name'], 26)
        subheading = truncate(track['artists'][0]['name'], 45)

        draw.text((10, 10), heading, fill=self.text_color, font=font_heading)
        draw.text((10, 250), subheading, fill=self.text_color, font=font_subheading)

        image.paste(track_image, (700, 0))
        return image

    def __str__(self):
        return f"{self._playing_track['item']['name']}"
