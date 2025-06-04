from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import re

def download_mp3(song_name, download_folder="downloads"):
    """
    Downloads an MP3 from xmwav.com based on the song name.

    Args:
        song_name: The name of the song to search for
        download_folder: Folder to save the downloaded MP3
    """
    # Create download directory if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)


    # Setup Chrome options
    chrome_options = Options()
    prefs = {"download.default_directory": os.path.abspath(download_folder)}
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Step 1: Go to search page and input song name
        driver.get("https://www.xmwav.com/index/search/")

        # Wait for search input to load and enter song name
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "edtSearch"))
        )
        search_input.clear()
        search_input.send_keys(song_name)
        search_input.send_keys(Keys.RETURN)

        # Step 2: Wait for search results and click the first result
        # 修正：根据新的HTML结构，<a>标签包含<li>，而不是<li>包含<a>
        result_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul > a[href*='/mscdetail/']"))
        )

        link_url = result_link.get_attribute("href")
        print(f"Found song link: {link_url}")
        result_link.click()

        # Step 3: 在歌曲详情页面获取所有包含download的a标签
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("=== 进入歌曲详情页面，开始查找包含download的a标签 ===")
        
        # 使用多种方式匹配，提高匹配度
        download_links = []
        
        # 方式1: href包含download（不区分大小写）
        links1 = driver.find_elements(By.XPATH, "//a[contains(translate(@href, 'DOWNLOAD', 'download'), 'download')]")
        download_links.extend(links1)
        print(f"方式1 - href包含download: 找到 {len(links1)} 个")
        
        # 方式2: 文本内容包含download（不区分大小写）
        links2 = driver.find_elements(By.XPATH, "//a[contains(translate(text(), 'DOWNLOAD', 'download'), 'download')]")
        download_links.extend(links2)
        print(f"方式2 - 文本包含download: 找到 {len(links2)} 个")
        
        # 方式3: class属性包含download
        links3 = driver.find_elements(By.XPATH, "//a[contains(@class, 'download')]")
        download_links.extend(links3)
        print(f"方式3 - class包含download: 找到 {len(links3)} 个")
        
        # 方式4: id属性包含download
        links4 = driver.find_elements(By.XPATH, "//a[contains(@id, 'download')]")
        download_links.extend(links4)
        print(f"方式4 - id包含download: 找到 {len(links4)} 个")
        
        # 方式5: 获取所有a标签，然后筛选
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href") or ""
            text = link.text or ""
            class_attr = link.get_attribute("class") or ""
            id_attr = link.get_attribute("id") or ""
            
            if ("download" in href.lower() or 
                "download" in text.lower() or 
                "download" in class_attr.lower() or 
                "download" in id_attr.lower()):
                if link not in download_links:
                    download_links.append(link)
        
        print(f"方式5 - 全部筛选后总计: {len(download_links)} 个")
        
        # 去重
        unique_links = []
        seen_hrefs = set()
        for link in download_links:
            href = link.get_attribute("href")
            if href and href not in seen_hrefs:
                unique_links.append(link)
                seen_hrefs.add(href)
        
        download_links = unique_links
        print(f"去重后: {len(download_links)} 个唯一链接")
        
        print("=== 所有包含download的a标签HTML ===")
        for i, link in enumerate(download_links):
            print(f"Link {i+1}: {link.get_attribute('outerHTML')}")
        
        # 提取所有链接的URL
        download_urls = []
        for link in download_links:
            href = link.get_attribute("href")
            if href:
                download_urls.append(href)
        
        print(f"\n=== 提取到的URL列表 ===")
        for i, url in enumerate(download_urls):
            print(f"URL {i+1}: {url}")
        
        # 检查是否有足够的链接
        if len(download_urls) < 2:
            print(f"警告：只找到 {len(download_urls)} 个download链接，需要至少2个")
            if len(download_urls) == 0:
                raise Exception("没有找到包含download的链接")
            # 如果只有一个链接，使用第一个
            selected_url = download_urls[0]
            print(f"使用第一个链接: {selected_url}")
        else:
            # 使用第二个URL链接
            selected_url = download_urls[1]
            print(f"使用第二个链接: {selected_url}")
        
        # 点击对应的链接
        target_link = None
        for link in download_links:
            if link.get_attribute("href") == selected_url:
                target_link = link
                break
        
        if target_link:
            print(f"点击链接: {selected_url}")
            target_link.click()
        else:
            print("无法找到对应的链接元素")
            return

        # Switch to the new tab (Quark pan page)
        # Wait a moment for the new tab to open
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])

        # Step 4: On the Quark pan page, find and click the download button
        download_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'download') or contains(text(), '下载')]"))
        )

        download_btn.click()

        # Wait for download to complete (this is a simple wait, could be improved)
        print("Waiting for download to complete...")
        time.sleep(10)

        print(f"Song '{song_name}' has been downloaded to {download_folder}")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    song_name = input("Enter the name of the song to download: ")
    download_mp3(song_name)
