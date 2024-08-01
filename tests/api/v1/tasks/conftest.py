import pytest


@pytest.fixture()
def yt_url_video():
    return "https://www.youtube.com/watch?v=2WZ5mN_tcAg"


@pytest.fixture()
def yt_url_playlist():
    return "https://www.youtube.com/playlist?list=PLySj34Zkq0TAdQTPMeGTGZafX-kqgoYbT"


@pytest.fixture()
def yt_url_channel():
    return "https://www.youtube.com/channel/UChJ4IOQrs63Y5_Rx5aqolZw"
