import requests
import json

print("=== Running Automated SEO & Technical Performance Diagnostics ===")

# Test Google PageSpeed Insights API (Public Endpoint)
api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://odontoscore.com/&category=PERFORMANCE&category=SEO&category=ACCESSIBILITY&category=BEST_PRACTICES&strategy=mobile"

try:
    print("Querying Google PageSpeed Insights API (Mobile Strategy)...")
    r = requests.get(api_url, timeout=30)
    if r.status_code == 200:
        data = r.json()
        cats = data.get("lighthouseResult", {}).get("categories", {})
        
        perf = cats.get("performance", {}).get("score", 0) * 100
        seo = cats.get("seo", {}).get("score", 0) * 100
        acc = cats.get("accessibility", {}).get("score", 0) * 100
        bp = cats.get("best-practices", {}).get("score", 0) * 100
        
        print("\n--- Google Lighthouse Official Scores (Mobile) ---")
        print(f"  🚀 SEO Score:            {int(seo)} / 100")
        print(f"  ⚡ Performance Score:    {int(perf)} / 100")
        print(f"  ♿ Accessibility Score:  {int(acc)} / 100")
        print(f"  🛡️ Best Practices Score: {int(bp)} / 100")
        
        audits = data.get("lighthouseResult", {}).get("audits", {})
        fcp = audits.get("first-contentful-paint", {}).get("displayValue", "N/A")
        lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
        cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
        tbt = audits.get("total-blocking-time", {}).get("displayValue", "N/A")
        
        print("\n--- Core Web Vitals Metrics ---")
        print(f"  FCP (First Contentful Paint):   {fcp}")
        print(f"  LCP (Largest Contentful Paint): {lcp}")
        print(f"  CLS (Cumulative Layout Shift):  {cls}")
        print(f"  TBT (Total Blocking Time):      {tbt}")
    else:
        print(f"PageSpeed API returned status: {r.status_code}")
except Exception as e:
    print(f"Error querying PageSpeed API: {e}")
