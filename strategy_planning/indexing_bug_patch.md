# 📊 전략기획부: 구글 서치 콘솔 & robots.txt 색인 오류 패치 체크리스트

웹사이트 색인 문제를 해결하고 애드센스 크롤러 유도를 위해 즉각 실행할 기술 점검 항목입니다.

## 1. robots.txt 최종 확인
현재 `https://insuretechlab.net/robots.txt` 파일 상태는 다음과 같습니다:
```plaintext
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: https://insuretechlab.net/sitemap_index.xml
```
* **상태**: 정상. 구글 봇의 수집을 명시적으로 거부하고 있지 않습니다.

---

## 2. 구글 서치 콘솔(Google Search Console) 소유권 인증 확인
색인이 0개인 원인은 사이트 등록 및 소유권 인증 단계에서 문제가 발생했을 확률이 높습니다.

- [ ] **구글 서치 콘솔 소유권 확인 방식 점검**
  - **HTML 태그 삽입**: 워드프레스 Rank Math 플러그인 설정 내 `웹마스터 도구` -> `Google Search Console` 코드 입력 여부 확인.
  - **DNS 레코드 등록**: 가비아 또는 도메인 구매 대행사에서 TXT 레코드가 정상적으로 등록되었는지 확인.
- [ ] **Sitemap 등록 상태 확인**
  - `sitemap_index.xml`을 제출했을 때 상태가 **'성공'**인지 확인 (만약 '가져올 수 없음' 빨간 에러가 뜬다면 Rank Math sitemap 캐싱 차단 해제 필요).

---

## 3. 애드센스 ads.txt 서빙 상태 확인
- [ ] 브라우저에서 `https://insuretechlab.net/ads.txt` 접속 시 애드센스 게시자 ID가 적힌 텍스트 파일이 올바르게 나타나는지 확인.
