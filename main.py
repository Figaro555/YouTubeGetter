import json

from googleapiclient.discovery import build
from Configs.configuration import api_key


def main():
    my_channels_id = ("UCsK1oV0PGkcZ1UhFtajx0dg",
                      "UC5Cpx_68IC6M60JPjsbpW4Q",
                      "UCq3PlGB0_e6jTc9Jr2Al7LQ",
                      "UCvKPc71Dd8qnuKZd2nRyH4g",

                      "UC8M5YVWQan_3Elm-URehz9w",
                      "UC6cqazSR6CnVMClY0bJI0Lg",
                      "UC87N76IGFB6Ib0Lo7omRgHw",
                      "UCCh8YfzvyPHugM0lkeQy54A",
                      "UCSaVoRErW4kqKsDqExs2MXA")

    youtube = build('youtube', 'v3', developerKey=api_key)

    result_json = {}

    for channel_id in my_channels_id:
        request = youtube.channels().list(
            part='statistics, snippet, contentDetails',
            id=channel_id
        )
        response = request.execute()

        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
            maxResults=5
        )
        pl_response = pl_request.execute()

        videos = {}
        for item in pl_response["items"]:
            v_request = youtube.videos().list(
                part='statistics, snippet',
                id=item["contentDetails"]["videoId"]
            )
            v_response = v_request.execute()

            videos[v_response["items"][0]['snippet']['title']] = {
                "viewCount": v_response["items"][0]['statistics']['viewCount'],
                "likeCount": v_response["items"][0]['statistics']['likeCount']}

        result_json[response["items"][0]['snippet']['title']] = {
            "viewCount": response["items"][0]['statistics']['viewCount'],
            "videoCount": response["items"][0]['statistics']['videoCount'],
            "videos": videos
        }
    s = json.dumps(result_json, indent=4, sort_keys=True, ensure_ascii=False)

    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == '__main__':
    main()
