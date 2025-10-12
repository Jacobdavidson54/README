# Student Research Bot: A High-End UX Web App for Academic Research
# 
# This Streamlit application provides an intuitive, modern interface for students to search 
# Google Scholar and the web. It fetches publication data from Google Scholar using the 'scholarly' 
# library and general web results using DuckDuckGo Search. The UI features a clean, responsive 
# design with expandable cards for results, search history, and customizable themes.
# New Feature: BibTeX export for Google Scholar results.
#
# Prerequisites:
# pip install streamlit scholarly duckduckgo-search
#
# Run with: streamlit run research_bot.py
#
# Note: 
# - Google Scholar scraping via 'scholarly' may require a proxy if rate-limited (uncomment proxy code).
# - Respect rate limits and terms of service. This is for educational use only.
# - For production, consider adding API keys for more robust search (e.g., SerpAPI for Scholar).

import streamlit as st
from scholarly import scholarly, ProxyGenerator
from duckduckgo_search import DDGS
import pandas as pd
from datetime import datetime
import re

# Function to generate BibTeX entry
def generate_bibtex(result, index):
    title = result.get('Title', 'Untitled')
    authors = result.get('Authors', 'Unknown Author')
    year = result.get('Year', 'N/A')
    url = result.get('URL', '')
    
    # Sanitize title for BibTeX (remove special characters)
    title = re.sub(r'[{}]', '', title)
    
    # Format authors for BibTeX
    author_list = authors.split(', ')
    bibtex_author = ' and '.join(author_list) if author_list else 'Unknown Author'
    
    # Generate BibTeX key (e.g., FirstAuthorYear)
    first_author = author_list[0].split()[-1] if author_list and author_list[0] else 'unknown'
    bibtex_key = f"{first_author}{year if year != 'N/A' else 'unknown'}{index}"
    
    # Build BibTeX entry
    bibtex = f"""@article{{{bibtex_key},
    title = {{{title}}},
    author = {{{bibtex_author}}},
    year = {{{year if year != 'N/A' else 'unknown'}}},
    url = {{{url if url else 'N/A'}}}
}}"""
    return bibtex

# Custom CSS for high-end UX: Modern, clean design with shadows, gradients, and smooth animations
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .search-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .search-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    .result-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .stExpander > div > div > div > div {
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Title and Header
st.markdown('<div class="main-header"><h1>🔬 Student Research Bot</h1><p>A sleek tool for discovering papers and web resources</p></div>', unsafe_allow_html=True)

# Sidebar for Controls
st.sidebar.title("⚙️ Settings")
search_type = st.sidebar.selectbox("Search Type", ["Google Scholar", "Web (DuckDuckGo)"])
num_results = st.sidebar.slider("Number of Results", 1, 10, 5)
use_proxy = st.sidebar.checkbox("Use Proxy (for Scholar rate limits)")

# Optional proxy setup for Scholar (uncomment and configure if needed)
if use_proxy:
    # pg = ProxyGenerator()
    # pg.FreeProxies()  # Or use paid proxies
    # scholarly.use_proxy(pg)
    st.sidebar.warning("Proxy setup requires manual configuration in code.")

# Search Input
query = st.text_input("Enter your research query:", placeholder="e.g., machine learning in healthcare")

# Search Button
if st.button("🚀 Search", type="primary", help="Initiate research discovery"):
    if query:
        with st.spinner("Fetching results..."):
            if search_type == "Google Scholar":
                # Search Google Scholar
                search_query = scholarly.search_pubs(query)
                results = []
                for i, result in enumerate(search_query):
                    if i >= num_results:
                        break
                    try:
                        pub = next(search_query)  # Fill details
                        results.append({
                            "Title": pub.get('bib', {}).get('title', 'N/A'),
                            "Authors": ", ".join(pub.get('bib', {}).get('author', [])),
                            "Year": pub.get('bib', {}).get('pub_year', 'N/A'),
                            "Cited By": pub.get('num_citations', 0),
                            "Abstract": pub.get('bib', {}).get('abstract', 'N/A'),
                            "URL": pub.get('eprint_url', pub.get('pub_url', 'N/A'))
                        })
                    except StopIteration:
                        break
                
                # Display Results
                st.subheader(f"📚 Scholar Results for '{query}'")
                for idx, result in enumerate(results):
                    with st.expander(f"**{result['Title']}** (Cited: {result['Cited By']})", expanded=False):
                        st.write(f"**Authors:** {result['Authors']}")
                        st.write(f"**Year:** {result['Year']}")
                        st.write(f"**Abstract:** {result['Abstract'][:200]}..." if len(result['Abstract']) > 200 else result['Abstract'])
                        if result['URL']:
                            st.markdown(f"[🔗 View Paper]({result['URL']})")
                        # BibTeX Export Button
                        bibtex_content = generate_bibtex(result, idx)
                        st.download_button(
                            label="📄 Download BibTeX",
                            data=bibtex_content,
                            file_name=f"citation_{idx+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bib",
                            mime="text/bib"
                        )
                
                # DataFrame for CSV Export
                if results:
                    df = pd.DataFrame(results)
                    st.download_button("📥 Download as CSV", df.to_csv(index=False), f"scholar_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

            else:  # Web Search
                # Search DuckDuckGo
                with DDGS() as ddgs:
                    web_results = [r for r in ddgs.text(query, max_results=num_results)]
                
                # Display Results
                st.subheader(f"🌐 Web Results for '{query}'")
                for result in web_results:
                    with st.expander(f"**{result['title']}**", expanded=False):
                        st.write(f"**Snippet:** {result['body'][:150]}...")
                        st.markdown(f"[🔗 Visit Site]({result['href']})")
                
                # DataFrame for CSV Export
                if web_results:
                    df = pd.DataFrame(web_results)
                    st.download_button("📥 Download as CSV", df.to_csv(index=False), f"web_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    else:
        st.warning("Please enter a query to start your research! 🎓")

# Footer
st.markdown("---")
st.markdown("*Built for students | Ethical use only | Data fetched in real-time*")

# Run the app
if __name__ == "__main__":
    st.rerun()  # Optional: Auto-rerun for dynamic updates