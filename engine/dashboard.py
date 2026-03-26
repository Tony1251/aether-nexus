import streamlit as st
from engine.shopify import ShopifyManager
from engine.database import TenantManager
from engine.pipeline import ProductionPipeline

st.title("AirArtshop 客户门户")

tenant_id = st.text_input("请输入您的 Tenant ID")

if tenant_id:
    tm = TenantManager(db_path="engine/tenants.db", key_path="engine/secret.key")
    token = tm.get_tenant_token(tenant_id)
    
    if token:
        st.success(f"已连接至店铺: {tenant_id}")
        keyword = st.selectbox("选择类目", ["silver earrings", "gold hoops", "minimalist jewelry"])
        
        if st.button("开始一键铺货"):
            with st.spinner("同步中..."):
                pipeline = ProductionPipeline(token)
                pipeline.run(keyword)
                st.success("同步已完成！")
    else:
        st.error("无效的订阅 ID")
