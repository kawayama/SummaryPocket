import json
import os

import dotenv
import streamlit as st
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from notion_client import helpers

from summary_pocket.services import notion

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.environ['OPENAI_API_TOKEN']
os.environ['OPENAI_ORGANIZATION'] = os.environ['OPENAI_API_ORGANIZATION']


def main():
    """メイン関数"""
    vectorstore = get_vectorstore()

    st.title('文書検索')
    text = st.text_input('検索するテキストを入力してください')

    if text:
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={'k': 5})
        results = retriever.invoke(text)
        for result in results:
            with st.chat_message('assistant'):
                st.write(result.metadata['title'])
                st.write(result.metadata['summary'])
                st.link_button(result.metadata['url'], result.metadata['url'])


@st.cache_resource
def get_vectorstore():
    """ベクトルストアを取得する"""
    # Notionからデータを取得
    client = notion._get_client()
    items = helpers.collect_paginated_api(client.databases.query, database_id=notion.NOTION_DB_ID)
    articles = [
        notion.NotionItem(
            is_read=item['properties']['is_read']['checkbox'],
            title=item['properties']['title']['title'][0]['plain_text'],
            url=item['properties']['url']['url'],
            category=item['properties']['category']['select']['name'],
            summary=item['properties']['summary']['rich_text'][0]['plain_text'],
            fetched_at=item['properties']['fetched_at']['date']['start'],
        )
        for item in items
        if item['properties']['url']['url'] is not None and item['properties']['category']['select'] is not None
    ]

    # ドキュメントを作成
    docs = []
    for article in articles:
        docs.append(
            Document(
                page_content=f"{article.title}\n{article.summary}",
                metadata=json.loads(article.model_dump_json()),
            )
        )

    # ドキュメントを分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits = text_splitter.split_documents(docs)

    return Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())


if __name__ == '__main__':
    main()
