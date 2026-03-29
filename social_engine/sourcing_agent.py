from adapters.aoxia import AoXiaAdapter

class SourcingAgent:
    def __init__(self):
        self.aoxia = AoXiaAdapter()

    def auto_source_products(self, keyword, limit=5):
        print(f"[*] 智能采购代理正在为 '{keyword}' 寻找货源...")
        self.aoxia.set_endpoint("opp.selection.newproduct.report/1.0")
        data = self.aoxia.execute({
            "productKeyword": keyword,
            "targetCountry": "US",
            "targetPlatform": "amazon",
            "userId": "0"
        })
        
        if data is None or 'result' not in data:
            print("[!] 选品接口返回空数据")
            return []
            
        products = data.get('result', {}).get('data', {}).get('productList', [])
        return products[:limit]
