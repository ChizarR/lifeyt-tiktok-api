from pprint import pprint

from tiktok_api import TikTokAPI


tiktok_api = TikTokAPI("./drivers/chromedriver")


def test_fetch_links_by_account_name():
    account = "@chipmunksoftiktok"
    return tiktok_api.fetch_account_links(account)


def test_fetch_links_by_tag():
    tag = "lions"
    return tiktok_api.fetch_tag_links(tag)


def test_download_video():
    link = "https://www.tiktok.com/@chipmunksoftiktok/video/6975140587196517638"
    return tiktok_api.get_video(link)


if __name__ == "__main__":
    print("-------- STARTED TEST --------\n")
    print("[INFO] - 1. Fetch data from account '@chipmunksoftiktok'...\n")
    pprint(test_fetch_links_by_account_name())
    print("\n-------- CONTINUE TEST --------\n")

    print("[INFO] - 2. Fetch data by tag 'lions'...\n")
    pprint(test_fetch_links_by_tag())
    print("\n-------- CONTINUE TEST --------\n")

    print("[INFO] - 3. Dowloading video by link...\n")
    pprint(test_download_video())
    print("\n-------- END OF TEST --------\n")
