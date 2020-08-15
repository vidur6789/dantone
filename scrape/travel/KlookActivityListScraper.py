import utils.scraperutils as utils
import utils.commonutils as cutils
import scrape.travel.KlookActivityDetailScraper as activity_scraper
import logging


def get_results():
    results = []
    for activity_type in [1, 3]:
        for page in range(1, 5):
            url = get_request_url(activity_type=activity_type, page=page)
            print(url)
            soup = utils.get_beautiful_soup(url)
            activity_list_tags = soup.find("div", class_="act_list")
            activities = [parse_activity(tag)for tag in activity_list_tags.children if is_valid_activity_tag(tag)]
            results.extend(activities)
            cutils.random_sleep(max_sleep=10)
    print(len(results))
    results = [result for result in results if result is not None]
    print(len(results))
    return results


def is_valid_activity_tag(tag):
    return tag.name == 'div' and tag.a["data-sold-out"] == 'false'


def get_request_url(city_id=6, activity_type=1, page="1"):
    url_template = "https://www.klook.com/en-SG/search/?container_type=city&type=city&city_id=6&template_id={template_id}&start={start}"
    return url_template.format(template_id=activity_type, city_id=city_id, start=page)


def parse_activity(activity_tag):
    try:
        url_prefix = "https://www.klook.com"
        li_tags = activity_tag.a.ul.find_all('li')
        price = li_tags[2].find("span", class_="latest_price").b.string.strip().split(" ")[1]
        rating = li_tags[1].span.span.span.string if li_tags[1].span.span is not None else "NA"
        num_booked_tag = li_tags[1].span if rating == "NA" else li_tags[1].span.next_sibling.next_sibling
        del_tag = li_tags[2].find("del")
        activity_dict = {"seo": activity_tag.a["data-url-seo"],
                         "name": activity_tag.h3.string,
                         "url": url_prefix + activity_tag.a["href"],
                         "image_url": activity_tag.a.div["data-original"],
                         "rating": li_tags[1].span.span.span.string if li_tags[1].span.span is not None else "NA",
                         "num_booked": li_tags[1].span.next_sibling.next_sibling.string.split(" ")[0].replace(",", "").replace("K", "000"),
                         "num_reviews": li_tags[1].span.span.next_sibling.next_sibling.string.split(" ")[0].lstrip("(").replace(",", ""),
                         "original_price": del_tag.span.next_sibling.string if del_tag is not None else price,
                         "price": price,
                         }
        activity_dict.update(activity_scraper.get_results(activity_dict["url"]))
        return activity_dict
    except Exception as e:
        logging.exception("Exception for {name}. Error logs:{xception}.\nActivity HTML content:\n{content}".format(name=activity_tag.h3.string,
                                                                                                                   xception=str(e),
                                                                                                                   content=str(activity_tag)))




