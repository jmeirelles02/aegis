import os
import streamlit as st
import requests

st.set_page_config(page_title="Aegis", layout="wide")

st.title("Aegis: Shadow Architect")
st.markdown("Valide sua arquitetura de software e dados.")

col_input, col_output = st.columns([1, 1])

with col_input:
    st.subheader("Configuração da Análise")
    title = st.text_input("Título do Sistema", value="API de E-commerce")
    description = st.text_area("Descrição da Arquitetura", height=200)
    
    analysis_types = st.multiselect(
        "Tipos de Análise",
        ["architecture", "security", "performance", "solid", "data_pipeline", "ai_system"],
        default=["architecture", "security"]
    )
    depth = st.selectbox("Profundidade", ["quick", "standard", "deep"], index=1)
    
    analyze_button = st.button("Executar Análise", type="primary")

with col_output:
    st.subheader("Resultados")
    if analyze_button:
        if not description:
            st.warning("Preencha a descrição da arquitetura.")
        else:
            payload = {
                "title": title,
                "description": description,
                "analysis_types": analysis_types,
                "depth": depth,
                "context": {}
            }
            
            with st.spinner("Analisando proposta..."):
                try:
                    api_url = os.getenv("API_URL", "http://localhost:8000")
                    response = requests.post(f"{api_url}/analyses/", json=payload)
                    
                    if response.status_code == 201:
                        data = response.json()
                        summary = data["summary"]
                        
                        st.metric(label="Score Geral", value=f"{summary['overall_score']}/100")
                        st.info(summary["verdict"])
                        
                        st.write("**Pontos Fortes**")
                        for strength in summary["strengths"]:
                            st.write(f"* {strength}")
                            
                        st.write("**Ganhos Rápidos**")
                        for win in summary["quick_wins"]:
                            st.write(f"* {win}")
                        
                        st.subheader("Descobertas Detalhadas")
                        for finding in data["findings"]:
                            with st.expander(f"[{finding['severity'].upper()}] {finding['title']}"):
                                st.write(f"**Categoria:** {finding['category']}")
                                st.write(f"**Descrição:** {finding['description']}")
                                st.write(f"**Recomendação:** {finding['recommendation']}")
                    else:
                        st.error(f"Erro na API: {response.text}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")