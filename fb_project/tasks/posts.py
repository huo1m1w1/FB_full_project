
import time
from ..scraper_tools import *




def run(key_words):
    # Initialize FacebookScraper
    scraper = FacebookScraper()

    # Set the target URL
    URL = "https://www.facebook.com/"

    # Log in to Facebook
    scraper.login(URL)

    # Create URL with search keys
    base_url = "https://www.facebook.com/search/posts/?q="
    url = create_url_with_keys(base_url, key_words)

    # load webpage with search keys to start scraping
    scraper.driver.get(url)

    time.sleep(5)

    input_element = scraper.find_element_with_wait(
        "XPATH", "//input[@placeholder='Posts from']"
    )
    input_element.click()

    time.sleep(5)
    # Find the span element with text 'Public posts' in the dropdown
    public_posts_element = scraper.find_element_with_wait(
        "XPATH", "//span[text()='Public posts']"
    )

    # Click on the 'Public posts' option in the dropdown
    public_posts_element.click()
    time.sleep(5)


    parent_element_xpath = (
        "//*[@id[starts-with(., 'mount_0_')] and descendant::*[@role='feed']]/"
        "div/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div"
    )
    NTH_OF_POSTS = 0
    NTH_OF_RECORDS = 0
    parent_element_xpath = "//*[@id[starts-with(., 'mount_0_')] and descendant::*[@role='feed']]/div/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div"

    while True:
        print(
            "..........................................................................."
        )
        print("")
        print("nth of post: ", NTH_OF_POSTS + 1)
        # 1. if possible move bottom of the element to the bottom of window
        # screen get all the posts
        all_posts = scraper.find_elements_with_wait(
            "XPATH",
            parent_element_xpath,
        )
        # position the post at right place
        scraper.position_the_element(all_posts[NTH_OF_POSTS])

        # 2. Get information of current element get all info of current element
        post_detail = all_posts[NTH_OF_POSTS].text
        # Get all reaction part
        reaction_list = post_detail.split("All reactions:")[-1].split("\n")

        # 3. if there are comments, collect post information and move the
        # bottom of element to the the bottom of the browser window
        # click comments button
        # initialise data of dictionary of post information

        post_info = {
            "SN": None,
            "Key words": "",
            "facebook url": "",
            "Author": "",
            "n_comments": 0,
            "Date of commnent": "",
            "Timestamp": "",
            "Comments": [],
        }

        if check_comments(reaction_list)[0]:
            # assign `n_comment` to post_info
            post_info["n_comments"] = check_comments(reaction_list)[1]
            comment_buton_xpath = (f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]'
                                   f'/div[1]/div[2]/div/div/div/div/div/div[{NTH_OF_POSTS+1}]'
                                   f'/div/div/div/div/div/div/div/div/div/div/div[8]/div/div'
                                   f'/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[2]/span')

            try:
                time.sleep(2)
                comment_clickable = WebDriverWait(scraper.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, comment_buton_xpath)))
                comment_clickable.click()

            except:
                time.sleep(3)
                print(f"An error occurred when opening comment pop up contains")

            post_xpath = (
                '//span[2]/span/a[@role="link"] | //span[4]/span/a[@role="link"]'
            )
            try:
                time.sleep(3)
                post_elems = scraper.find_elements_with_wait("XPATH", post_xpath)
                if len(post_elems) == 1:
                    post_elems[0].click()
                else:
                    post_elems[-1].click()
                    time.sleep(5)

            except Exception as e:
                print("post element are not found: ", e)

            # scraper.click_element_with_retry()
            # scraper.click_all_comments_button()

            post_url = scraper.driver.current_url
            post_hash_match = re.search(r"/posts/([^/?]+)", post_url)
            if not post_hash_match:
                scraper.driver.back()
                time.sleep(5)
                close_button = scraper.find_elements_with_wait(
                    "CSS_SELECTOR", 'div > div[aria-label="Close"]'
                )
                time.sleep(1)
                # Click the button
                close_button[-1].click()
                video_post_hash_match = re.search(r"/videos/([^/?]+)", post_url)
                if video_post_hash_match:
                    video_close_button = scraper.find_element_with_wait(
                        "CSS_SELECTOR", '[aria-label="Close Video and scroll"]'
                    )
                    video_close_button.click()
                NTH_OF_POSTS += 1
                print("post_info: ", post_info)
                print("post_url: ", post_url)
                print("post url doesn't meet requirement, move on to next post")
                continue

            try:
                # Wait again for the span element after scrolling
                time.sleep(3)
                scraper.find_element_with_wait(
                    "XPATH", '//span[text()="Top comments" or text()="Most relevant"]'
                ).click()

            except Exception as e:
                print(f"Comment selection button not found even after scrolling: {e}")
                # driver.quit()

            # Click on the element with text "Top comments" or "All comments" using explicit wait
            try:
                time.sleep(3)
                all_comments_button = scraper.find_element_with_wait(
                    "XPATH", '//span[text()="All comments" or text()="Oldest"]'
                )
                all_comments_button.click()
                time.sleep(5)
            except Exception as e:
                print(f"Error clicking on all comments button: {e}")
                pass
            # get author information
            author_elem_xpath = "//span/h2/span[1]/a/strong/span"
            try:
                author_elem = scraper.find_element_with_wait("XPATH", author_elem_xpath)
                post_info["Author"] = author_elem.text

            except Exception as e:
                print("No author name found")
                post_info["Author"] = ""

            post_info["SN"] = NTH_OF_RECORDS + 1
            post_info["Key words"] = key_words
            post_info["facebook url"] = post_url

            original_position = scraper.driver.execute_script("return window.scrollY;")

            while True:
                try:
                    # body = scraper.driver.find_element("body")
                    # body.send_keys(ke        Keys.PAGE_DOWN)
                    scraper.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight)"
                    )
                    time.sleep(5)
                    view_more_button = WebDriverWait(scraper.driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//span[contains(text(), " more comments")]')
                        )
                    )
                    view_more_button.click()
                    time.sleep(8)

                except Exception:
                    print("No more comments!")
                    break
            number_of_extendable_comments = 0
            while True:
                try:
                    scraper.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(3)

                    extenable_elements = scraper.get_extension_elements()
                    print("(extenable_elements)", len(extenable_elements))
                    if len(extenable_elements) == number_of_extendable_comments:
                        break

                    scraper.get_extension(
                        extenable_elements
                    )  # clicking on see more and opening the comment
                    number_of_extenable_comments = len(extenable_elements)
                    time.sleep(4)

                except Exception as e:
                    print("No more extensions: ", e)
                    break

            all_comment_elements = scraper.find_elements_with_wait(
                "XPATH", '//div[contains(@aria-label, "Comment by")]'
            )
            all_comment_contains = []
            scraper.comment_reply_titles = [
                comment_elem.get_attribute("aria-label")
                for comment_elem in all_comment_elements
            ]
            for comment_element in all_comment_elements:
                comments = scraper.collect_comments_replies(comment_element)

                all_comment_contains.append(comments)

            post_info["Comments"] = all_comment_contains

            dt = datetime.now()
            post_info["Timestamp"] = datetime.timestamp(dt)

            time.sleep(3)

            scraper.driver.execute_script(f"window.scrollTo(0, {original_position});")

            scraper.driver.back()
            time.sleep(5)

            print("post_info:", post_info)

            try:
                with open("data_list.json") as file:
                    existing_data_list = json.load(file)
            except FileNotFoundError:
                existing_data_list = []

            # Append the new dictionary to the list
            existing_data_list.append(post_info)

            # Write the updated list of dictionaries back to the file
            with open("data_list.json", "w") as file:
                json.dump(existing_data_list, file, indent=2)

            # filename = "data_list.json"
            # await save_to_json(post_info, filename)
            scraper.close_popup()
            
            NTH_OF_RECORDS += 1

            if NTH_OF_RECORDS == 20:
                scraper.driver.quit()
                break
        
        NTH_OF_POSTS += 1


