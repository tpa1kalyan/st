from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Path to your ChromeDriver
driver_path = "D:/sel/chromedriver-win64/chromedriver.exe"

service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

try:
    # Go to Google and search
    driver.get("https://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("net speed test")
    search_box.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 30)

    # Robust, case-insensitive XPath for "Run speed test" that matches button/a/role=button
    xpath_run = ("//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                 "'abcdefghijklmnopqrstuvwxyz'),'run speed test') and "
                 "(local-name() = 'button' or local-name() = 'a' or @role='button')]")

    clicked = False

    # Try to find and click the run button in the main document
    try:
        run_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_run)))
        driver.execute_script("arguments[0].click();", run_btn)
        clicked = True
    except Exception:
        # If not found in main document, search inside any iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                # short explicit wait inside iframe
                run_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath_run)))
                driver.execute_script("arguments[0].click();", run_btn)
                clicked = True
                driver.switch_to.default_content()
                break
            except Exception:
                driver.switch_to.default_content()
                continue

    if not clicked:
        raise Exception("Run speed test button not found/clickable")

    # Wait a bit for the test to start
    time.sleep(1)

    # Poll results and print live updates until stable
    driver.switch_to.default_content()

    # --- CHANGED: improved extraction across main doc + iframes, wait for numeric results ---
    def gather_texts():
        texts = []
        # main document text
        try:
            main_text = driver.execute_script("return document.body ? document.body.innerText : ''")
            if main_text:
                texts.append(main_text)
        except Exception:
            pass

        # attempt to read same-origin iframe documents; if cross-origin, gather attributes as fallback
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                # try to access iframe document body text
                frame_text = driver.execute_script(
                    "return arguments[0].contentDocument && arguments[0].contentDocument.body ? arguments[0].contentDocument.body.innerText : ''",
                    iframe,
                )
                if frame_text:
                    texts.append(frame_text)
                    continue
            except Exception:
                # cross-origin or access blocked; fall back to iframe attributes that might contain helpful labels
                try:
                    attrs = []
                    title = iframe.get_attribute("title")
                    if title:
                        attrs.append(title)
                    aria = iframe.get_attribute("aria-label")
                    if aria:
                        attrs.append(aria)
                    src = iframe.get_attribute("src")
                    if src:
                        attrs.append(src)
                    combined = " ".join(a for a in attrs if a)
                    if combined:
                        texts.append(combined)
                except Exception:
                    pass

        # split texts into lines for easier nearest-label scanning
        lines = []
        for t in texts:
            for line in t.splitlines():
                s = line.strip()
                if s:
                    lines.append(s)
        return lines

    def find_near_label(lines, label_re, value_re, window=8):
        for i, line in enumerate(lines):
            if re.search(label_re, line, re.I):
                end = min(i + window + 1, len(lines))
                # check same line first
                m = re.search(value_re, line, re.I)
                if m:
                    return m.group(1).strip()
                # then forward lines
                for j in range(i + 1, end):
                    m = re.search(value_re, lines[j], re.I)
                    if m:
                        return m.group(1).strip()
        return None

    # broader patterns: capture numbers optionally followed/preceded by units
    mbps_re = r'(\d+(?:\.\d+)?\s*(?:mbps|Mbps|Mbit/s|Mbps)?)'
    ms_re = r'(\d+(?:\.\d+)?\s*(?:ms)?)'
    any_num_re = r'(\d+(?:\.\d+)?)'

    # wait up to first_value_timeout for any numeric result to appear in page/frames
    first_value_timeout = 30
    try:
        WebDriverWait(driver, first_value_timeout).until(
            lambda d: bool(re.search(r'\d+(?:\.\d+)?\s*(Mbps|mbps|ms|Mbit/s)', d.execute_script("return document.body ? document.body.innerText : ''") or ""))
        )
    except Exception:
        # continue anyway; sometimes results are in iframes we can't poll via JS
        pass

    timeout = 120
    start_time = time.time()
    prev_vals = ("", "", "", "")
    stable_count = 0
    print("Waiting for speed readings... (press Ctrl+C to abort)")

    while time.time() - start_time < timeout and stable_count < 3:
        try:
            lines = gather_texts()

            # try reliable label-based matches
            d = find_near_label(lines, r'\bdownload\b', mbps_re) or ""
            u = find_near_label(lines, r'\bupload\b', mbps_re) or ""
            p = find_near_label(lines, r'\bping\b|\blatency\b', ms_re) or ""
            j = find_near_label(lines, r'\bjitter\b', ms_re) or ""

            # fallback: collect standalone Mbps or ms occurrences in order
            if not (d and u):
                all_mbps = []
                for line in lines:
                    for m in re.finditer(mbps_re, line, re.I):
                        all_mbps.append(m.group(1).strip())
                if all_mbps:
                    d = d or (all_mbps[0] if len(all_mbps) >= 1 else "")
                    u = u or (all_mbps[1] if len(all_mbps) >= 2 else "")

            # another fallback: any numbers with "download/upload" nearby in same line
            if not d:
                for line in lines:
                    if re.search(r'download', line, re.I) and re.search(any_num_re, line):
                        m = re.search(any_num_re, line)
                        if m:
                            d = m.group(1) + " Mbps"
                            break
            if not u:
                for line in lines:
                    if re.search(r'upload', line, re.I) and re.search(any_num_re, line):
                        m = re.search(any_num_re, line)
                        if m:
                            u = m.group(1) + " Mbps"
                            break

            current = (d, u, p, j)
            print(f"\rDownload: {d or '-'} | Upload: {u or '-'} | Ping: {p or '-'} | Jitter: {j or '-'}", end="", flush=True)

            if current == prev_vals and any(current):
                stable_count += 1
            else:
                stable_count = 0

            prev_vals = current
        except KeyboardInterrupt:
            print("\nAborted by user.")
            break
        except Exception:
            # ignore transient errors
            pass

        time.sleep(1)

    print()
    final_download, final_upload, final_ping, final_jitter = prev_vals
    print("Final readings:")
    print("  Download Speed:", final_download or "N/A")
    print("  Upload Speed:  ", final_upload or "N/A")
    if(int(final_download)>30):
        print("high resolution videos can be streamed")
    elif(int(final_download)<20):
        print("medium resolution videos can be streamed and low resolution videos can be downloadable")
    # --- END CHANGED ---
finally:
    driver.quit()
