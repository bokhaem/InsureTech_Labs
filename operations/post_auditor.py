import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
import re

SITEMAP_URL = "https://insuretechlab.net/post-sitemap.xml"

AI_SMELL_KEYWORDS = [
    "알아보겠습니다",
    "안녕하세요",
    "결론적으로",
    "요약하자면",
    "이 글에서는",
    "첫째,",
    "둘째,",
    "셋째,",
    "마지막으로",
    "주의해야 할 점",
]

def fetch_urls_from_sitemap(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers)
    root = ET.fromstring(response.content)
    urls = []
    for sitemap in root:
        for loc in sitemap.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            urls.append(loc.text)
    return urls

def analyze_post(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # main content is usually inside an article tag or .entry-content
        content_div = soup.find('div', class_='entry-content') or soup.find('article')
        if not content_div:
            return None
        
        text = content_div.get_text(separator=' ')
        
        word_count = len(text.replace(" ", ""))
        
        ai_smell_count = 0
        detected_keywords = []
        for kw in AI_SMELL_KEYWORDS:
            count = text.count(kw)
            if count > 0:
                ai_smell_count += count
                detected_keywords.append(kw)
                
        h2_count = len(content_div.find_all('h2'))
        h3_count = len(content_div.find_all('h3'))
        
        grade = "A (우수)"
        if word_count < 1000 or ai_smell_count > 3:
            grade = "D (위험)"
        elif word_count < 1500 or ai_smell_count > 1:
            grade = "C (경고)"
        elif ai_smell_count > 0:
            grade = "B (보통)"
            
        return {
            "url": url,
            "title": soup.title.string if soup.title else url,
            "word_count": word_count,
            "ai_smell_count": ai_smell_count,
            "detected_keywords": detected_keywords,
            "h2": h2_count,
            "h3": h3_count,
            "grade": grade
        }
    except Exception as e:
        print(f"Error on {url}: {e}")
        return None

def main():
    print("Fetching sitemap...")
    try:
        urls = fetch_urls_from_sitemap(SITEMAP_URL)
        print(f"Found {len(urls)} URLs. Starting analysis...")
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return
    
    results = []
    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Analyzing {url} ...")
        res = analyze_post(url)
        if res:
            results.append(res)
        time.sleep(0.3) # prevent server rate limit
        
    # Generate Markdown Report
    report_path = "d:/antigravity/InsureTech_Labs/strategy_planning/heuristic_audit_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 블로그 79개 포스팅 전수 로컬 검수 보고서 (API 우회 방식)\n\n")
        f.write(f"총 분석 포스팅: {len(results)}건\n\n")
        f.write("## 요약 통계\n")
        
        grade_counts = {"A (우수)":0, "B (보통)":0, "C (경고)":0, "D (위험)":0}
        total_words = 0
        
        for r in results:
            if r['grade'] in grade_counts:
                grade_counts[r['grade']] += 1
            total_words += r['word_count']
            
        avg_words = total_words / len(results) if len(results) > 0 else 0
        
        for g, c in grade_counts.items():
            f.write(f"- {g}: {c}건\n")
        f.write(f"\n- **평균 글자수**: {int(avg_words)}자 (공백 제외)\n\n")
            
        f.write("## 상세 분석 결과\n\n")
        f.write("| No | URL | 글자수(공백제외) | 기계적 키워드 수 | 발견된 키워드 | H2/H3 수 | 등급 |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        for i, r in enumerate(results):
            kw_str = ", ".join(r['detected_keywords']) if r['detected_keywords'] else "없음"
            f.write(f"| {i+1} | [Link]({r['url']}) | {r['word_count']} | {r['ai_smell_count']} | {kw_str} | {r['h2']}/{r['h3']} | **{r['grade']}** |\n")
            
    print(f"\nAnalysis complete. Saved to {report_path}")

if __name__ == "__main__":
    main()
